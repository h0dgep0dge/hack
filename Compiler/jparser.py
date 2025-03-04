from jlexer import TokenType

BinaryOperators = [TokenType.PLUS,  TokenType.MINUS, TokenType.STAR,
                   TokenType.SLASH, TokenType.AMPER, TokenType.PIPE,
                   TokenType.LTHAN, TokenType.GTHAN, TokenType.EQUAL]
UnaryOperators = [TokenType.MINUS,TokenType.TILDE]

VarDatatypes = [TokenType.INT,TokenType.CHAR,TokenType.BOOL,TokenType.IDENT]
SubroutineDatatypes = [TokenType.INT,TokenType.CHAR,TokenType.BOOL,TokenType.VOID,TokenType.IDENT]

def printer(func):
    def wrapper_func(self):
        print(func.__name__)
        func(self)
    return wrapper_func

class JParser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.ptr = 0
    
    def is_empty(self):
        return self.ptr >= len(self.tokens)
    
    def is_not_empty(self):
        return not self.is_empty()
    
    def peek(self,offset=0):
        if self.ptr+offset >= len(self.tokens):
            raise Exception("Unexpected end of file")
        return self.tokens[self.ptr+offset]

    def chop(self):
        r = self.peek()
        self.ptr += 1
        return r

    def expect(self,*args):
        if self.is_empty():
            raise Exception("Unexpected end of file")
        if self.peek().type in args:
            return self.chop()
        raise Exception("Unexpected token",self.peek())

    @printer
    def jclass(self):
        self.expect(TokenType.CLASS)
        self.expect(TokenType.IDENT)
        self.expect(TokenType.LBRACE)
        self.classVarDecs()
        self.subroutineDecs()
        self.expect(TokenType.RBRACE)

    @printer
    def classVarDecs(self):
        while self.peek().type is TokenType.STATIC or \
              self.peek().type is TokenType.FIELD:
            self.expect(TokenType.STATIC,TokenType.FIELD)
            self.expect(*VarDatatypes)
            self.expect(TokenType.IDENT)
            while self.peek().type is TokenType.COMMA:
                self.expect(TokenType.COMMA)
                self.expect(TokenType.IDENT)
            self.expect(TokenType.SEMIC)
    
    @printer
    def subroutineDecs(self):
        self.expect(TokenType.CONSTR,TokenType.FUNC,TokenType.METH)
        self.expect(*SubroutineDatatypes)
        self.expect(TokenType.IDENT)
        self.expect(TokenType.LPAREN)
        if self.peek().type in VarDatatypes:
            self.expect(*VarDatatypes)
            self.expect(TokenType.IDENT)
            while self.peek().type is TokenType.COMMA:
                self.expect(TokenType.COMMA)
                self.expect(*VarDatatypes)
                self.expect(TokenType.IDENT)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        
        while self.peek().type is TokenType.VAR:
            self.expect(TokenType.VAR)
            self.expect(*VarDatatypes)
            self.expect(TokenType.IDENT)
            while self.peek().type is TokenType.COMMA:
                self.expect(TokenType.COMMA)
                self.expect(TokenType.IDENT)
            self.expect(TokenType.SEMIC)

        self.statements()

        self.expect(TokenType.RBRACE)

    @printer
    def statements(self):
        while self.peek().type in [TokenType.LET,TokenType.IF,TokenType.WHILE,TokenType.DO,TokenType.RETURN]:
            match self.peek().type:
                case TokenType.LET:
                    self.letStatement()
                case TokenType.IF:
                    self.ifStatement()
                case TokenType.WHILE:
                    self.whileStatement()
                case TokenType.DO:
                    self.doStatement()
                case TokenType.RETURN:
                    self.returnStatement()

    @printer
    def letStatement(self):
        self.expect(TokenType.LET)
        self.expect(TokenType.IDENT)
        if self.peek().type is TokenType.LBRACK:
            self.expect(TokenType.LBRACK)
            self.expr()
            self.expect(TokenType.RBRACK)
        self.expect(TokenType.EQUAL)
        self.expr()
        self.expect(TokenType.SEMIC)

    @printer
    def ifStatement(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        self.expr()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        self.statements()
        self.expect(TokenType.RBRACE)
        if self.peek().type is TokenType.ELSE:
            self.expect(TokenType.LBRACE)
            self.statements()
            self.expect(TokenType.RBRACE)

    @printer
    def whileStatement(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        self.expr()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        self.statements()
        self.expect(TokenType.RBRACE)

    @printer
    def doStatement(self):
        self.expect(TokenType.DO)
        self.subrCall()
        self.expect(TokenType.SEMIC)

    @printer
    def returnStatement(self):
        self.expect(TokenType.RETURN)
        if self.peek().type is not TokenType.SEMIC:
            self.expr()
        self.expect(TokenType.SEMIC)
    
    @printer
    def expr(self):
        self.term()
        self.rexpr()
    
    @printer
    def rexpr(self):
        if self.peek().type is TokenType.PLUS:
            self.expect(TokenType.PLUS)
            self.term()
            self.rexpr()
            return
        if self.peek().type is TokenType.MINUS:
            self.expect(TokenType.MINUS)
            self.term()
            self.rexpr()
            return
        'Epsilon'
        return

    @printer
    def term(self):
        self.factor()
        self.rterm()
    
    @printer
    def rterm(self):
        if self.peek().type is TokenType.STAR:
            self.expect(TokenType.STAR)
            self.factor()
            self.rterm()
            return
        if self.peek().type is TokenType.SLASH:
            self.expect(TokenType.SLASH)
            self.factor()
            self.rterm()
            return
        'Epsilon'
        return
    
    @printer
    def factor(self):
        if self.peek().type is TokenType.INTLIT:
            self.expect(TokenType.INTLIT)
            return
        if self.peek().type is TokenType.STRLIT:
            self.expect(TokenType.STRLIT)
            return
        if self.peek().type is TokenType.IDENT and (self.peek(1).type is TokenType.LPAREN or self.peek(1).type is TokenType.DOT):
            self.subrCall()
            return
        if self.peek().type is TokenType.IDENT:
            self.expect(TokenType.IDENT)
            if self.peek().type is TokenType.LBRACK:
                self.expect(TokenType.LBRACK)
                self.expr()
                self.expect(TokenType.RBRACK)
            return
        if self.peek().type is TokenType.MINUS:
            self.expect(TokenType.MINUS)
            self.factor()
            return
        if self.peek().type is TokenType.LPAREN:
            self.expect(TokenType.LPAREN)
            self.expr()
            self.expect(TokenType.RPAREN)
        raise Exception("Unexpected token",self.peek())
    
    @printer
    def subrCall(self):
        self.expect(TokenType.IDENT)
        if self.peek().type is TokenType.DOT:
            self.expect(TokenType.DOT)
            self.expect(TokenType.IDENT)
        self.expect(TokenType.LPAREN)
        if self.peek().type is not TokenType.RPAREN:
            self.expr()
            while self.peek().type is TokenType.COMMA:
                self.expect(TokenType.COMMA)
                self.expr()
        self.expect(TokenType.RPAREN)

        
        
