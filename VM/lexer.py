from enum import Enum
import string

class TokenType(Enum):
    IDENT = 0
    NUMBER = 1
    NEWLINE = 2

class Token:
    def __init__(self,type,source,line):
        self.type = type
        self.source = source
        self.line = line
    
    def __repr__(self):
        if self.type == TokenType.NEWLINE:
            return "Token( type=TokenType." + self.type.name + " , source=\"\\n\" , line=" + str(self.line) + " )"
        return "Token( type=TokenType." + self.type.name + " , source=\"" + self.source + "\" , line=" + str(self.line) + " )"

class VMLexer:


    def __init__(self,source):
        self.source = source
        self.ptr = 0
        self.line = 1
    
    def is_empty(self):
        return self.ptr >= len(self.source)

    def is_not_empty(self):
        return not self.is_empty()

    def peek(self):
        if self.is_empty():
            return None
        return self.source[self.ptr]
    
    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
        return r

    def chop_number(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in string.digits:
            self.chop()
        return Token(TokenType.NUMBER,self.source[start:self.ptr],self.line)


    def chop_ident(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in (string.ascii_letters + string.digits + "_.$:-"):
            self.chop()
        return Token(TokenType.IDENT,self.source[start:self.ptr],self.line)

    def dump_line(self):
        while self.is_not_empty() and self.peek() != "\n":
            self.chop()

    def next_token(self):
        while self.is_not_empty() and self.peek().isspace():
            if self.chop() == "\n":
                self.line += 1
                return Token(TokenType.NEWLINE,"\n",self.line-1)
            
        if self.is_empty():
            return None
        
        if self.peek() in string.digits:
            return self.chop_number()
        if self.peek() in string.ascii_letters:
            return self.chop_ident()
        if self.peek() == "/":
            self.chop()
            if self.peek() == "/":
                self.dump_line()
                return self.next_token()
            raise Exception("Illegal single slash",self.line)
        raise Exception("Unknown character",self.peek())
        
