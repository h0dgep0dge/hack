import string

class Token:
    names = ["AT","NUMBER","NAME","LPAREN","RPAREN","EQUAL","SEMICO","MINUS","PLUS","EXCLAM","AMPER","PIPE","UNKNOWN"]
    AT = 0
    NUMBER = 1
    NAME = 2
    LPAREN = 3
    RPAREN = 4
    EQUAL = 5
    SEMICO = 6
    MINUS = 7
    PLUS = 8
    EXCLAM = 9
    AMPER = 10
    PIPE = 11
    UNKNOWN = 12

    def __init__(self,type,value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return self.names[self.type] + " " + self.value

class Lexer:

    def __init__(self,source):
        self.ptr = 0
        self.source = source
    
    def is_empty(self):
        return self.ptr >= len(self.source)
    
    def is_not_empty(self):
        return not self.is_empty()

    def peek(self):
        return None if self.is_empty() else self.source[self.ptr]
    
    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
        return r

    def trim(self):
        while self.is_not_empty() and self.peek().isspace():
            self.chop()
    
    def dump_line(self):
        while self.is_not_empty() and self.chop() != "\n":
            pass
    
    def make_number(self):
        r = ""
        while self.is_not_empty() and self.peek() in string.digits:
            r += self.chop()
        return Token(Token.NUMBER,r)
    
    def make_name(self):
        r = ""
        while self.is_not_empty() and self.peek() in string.digits+string.ascii_letters+"_.$:":
            r += self.chop()
        return Token(Token.NAME,r)

    def next_token(self):
        self.trim()
        if self.is_empty():
            return None
        match self.peek():
            case "@":
                return Token(Token.AT,self.chop())
            case "(":
                return Token(Token.LPAREN,self.chop())
            case ")":
                return Token(Token.RPAREN,self.chop())
            case "=":
                return Token(Token.EQUAL,self.chop())
            case ";":
                return Token(Token.SEMICO,self.chop())
            case "-":
                return Token(Token.MINUS,self.chop())
            case "+":
                return Token(Token.PLUS,self.chop())
            case "!":
                return Token(Token.EXCLAM,self.chop())
            case "&":
                return Token(Token.AMPER,self.chop())
            case "|":
                return Token(Token.PIPE,self.chop())
            case "|":
                return Token(Token.PIPE,self.chop())
            case "/":
                self.dump_line()
                return self.next_token()
        if self.peek() in string.digits:
            return self.make_number()
        if self.peek() in string.ascii_letters+"_.$:":
            return self.make_name()
                
class AInstruction:
    pass


source = ""
with open("fibNL.asm") as f:
    for line in f:
        source += line

lex = Lexer(source)
tokens = []

token = lex.next_token()
while token != None:
    tokens.append(token)
    token = lex.next_token()

print(tokens)