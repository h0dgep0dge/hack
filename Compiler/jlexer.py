from enum import Enum
import string

class TokenType(Enum):
    CLASS = 0
    CONSTR = 1
    FUNC = 2
    METH = 3
    FIELD = 4
    STATIC = 5
    VAR = 6
    INT = 7
    CHAR = 8
    BOOL = 9
    VOID = 10
    TRUE = 12
    FALSE = 13
    NULL = 14
    THIS = 15
    LET = 16
    DO = 17
    IF = 18
    ELSE = 19
    WHILE = 20
    RETURN = 21
    LBRACE = 22
    RBRACE = 23
    LPAREN = 24
    RPAREN = 25
    LBRACK = 25
    RBRACK = 26
    DOT = 27
    COMMA = 28
    SEMIC = 29
    PLUS = 30
    MINUS = 31
    STAR = 32
    SLASH = 33
    AMPER = 34
    PIPE = 35
    LTHAN = 36
    GTHAN = 37
    EQUAL = 38
    TILDE = 39
    INTLIT = 40
    STRLIT = 41
    IDENT = 42
    UNKNOWN = 43

class Token:
    def __init__(self,type,source):
        self.type = type
        self.source = source
    
    def __repr__(self):
        return f"Token( {self.type} , \"{self.source}\" )"

class JLexer:
    def __init__(self,source):
        self.source = source
        self.ptr = 0
        self.line = 1
    
    def is_empty(self):
        return self.ptr >= len(self.source)
    
    def is_not_empty(self):
        return not self.is_empty()
    
    def peek(self,offset=0):
        if self.ptr+offset >= len(self.source):
            return None
        return self.source[self.ptr+offset]

    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
            if r == "\n":
                self.line += 1
        return r

    def chop_ident(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in string.ascii_letters + string.digits + "_":
            self.chop()
        # TODO add some logic to find keywords
        return Token(TokenType.IDENT,self.source[start:self.ptr])

    def chop_intlit(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in string.digits:
            self.chop()
        return Token(TokenType.INTLIT,self.source[start:self.ptr])

    def chop_strlit(self):
        start = self.ptr
        self.chop() # Should be ", but what if it isn't? Should I be throwing an error here?
        while self.is_not_empty() and self.chop() != '"':
            pass
        return Token(TokenType.STRLIT,self.source[start:self.ptr])
    
    def chop_line(self):
        while self.is_not_empty() and self.chop() != "\n":
            pass
    
    def chop_comment(self):
        while self.is_not_empty():
            if self.chop() == "*" and self.chop() == "/":
                break

    def next_token(self):
        while self.is_not_empty() and self.peek().isspace():
            self.chop()
        if self.is_empty():
            return None
        c = self.peek()
        
        match c:
            case "{":
                return Token(TokenType.LBRACE,self.chop())
            case "}":
                return Token(TokenType.RBRACE,self.chop())
            case "(":
                return Token(TokenType.LPAREN,self.chop())
            case ")":
                return Token(TokenType.RPAREN,self.chop())
            case "[":
                return Token(TokenType.LBRACK,self.chop())
            case "]":
                return Token(TokenType.RBRACK,self.chop())
            case ".":
                return Token(TokenType.DOT,self.chop())
            case ",":
                return Token(TokenType.COMMA,self.chop())
            case ";":
                return Token(TokenType.SEMIC,self.chop())
            case "+":
                return Token(TokenType.PLUS,self.chop())
            case "-":
                return Token(TokenType.MINUS,self.chop())
            case "*":
                return Token(TokenType.STAR,self.chop())
            case "/":

                if self.peek(1) == "/":
                    self.chop_line()
                    return self.next_token()
                if self.peek(1) == "*":
                    self.chop_comment()
                    return self.next_token()
                return Token(TokenType.SLASH,self.chop())
            case "&":
                return Token(TokenType.AMPER,self.chop())
            case "|":
                return Token(TokenType.PIPE,self.chop())
            case "<":
                return Token(TokenType.LTHAN,self.chop())
            case ">":
                return Token(TokenType.GTHAN,self.chop())
            case "=":
                return Token(TokenType.EQUAL,self.chop())
            case "~":
                return Token(TokenType.TILDE,self.chop())
            case '"':
                return self.chop_strlit()
        if c in string.digits:
            return self.chop_intlit()
        if c == "_" or c in string.ascii_letters:
            return self.chop_ident()
        return Token(TokenType.UNKNOWN,self.chop())