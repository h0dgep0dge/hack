from jlexer import TokenType
from progclasses import *

BinaryOperators = [TokenType.PLUS,  TokenType.MINUS, TokenType.STAR,
                   TokenType.SLASH, TokenType.AMPER, TokenType.PIPE,
                   TokenType.LTHAN, TokenType.GTHAN, TokenType.EQUAL]
UnaryOperators = [TokenType.MINUS,TokenType.TILDE]

VarDatatypes = [TokenType.INT,TokenType.CHAR,TokenType.BOOL,TokenType.IDENT]
SubroutineDatatypes = [TokenType.INT,TokenType.CHAR,TokenType.BOOL,TokenType.VOID,TokenType.IDENT]

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
        if r is not None:
            self.ptr += 1
            if r == "\n":
                self.line += 1
        return r

    def expect(self,*args):
        if self.is_empty():
            raise Exception("Unexpected end of file")
        if self.peek().type in args:
            return self.chop()
        raise Exception("Unexpected token",self.peek())

    def chop_expression(self):
        term = self.chop_term()
        opterms = []
        while self.is_not_empty() and self.peek().type in BinaryOperators:
            op = self.chop()
            subterm = self.chop_term()
            opterms.append((op,subterm))
        return Expression(term,opterms)
    
    def chop_subscript(self):
        ident = self.expect(TokenType.IDENT)
        self.expect(TokenType.LBRACK)
        index = self.chop_expression()
        self.expect(TokenType.RBRACK)
        return SubscriptTerm(ident,index)

    def chop_subroutine(self):
        print(f"Chopping subroutine call at {self.tokens[self.ptr]}")
        subroutineName = None
        className = None
        first = self.expect(TokenType.IDENT)
        if self.peek().type is TokenType.DOT:
            className = first
            self.expect(TokenType.DOT)
            subroutineName = self.expect(TokenType.IDENT)
        else:
            subroutineName = first
        self.expect(TokenType.LPAREN)
        if self.peek().type is TokenType.RPAREN:
            self.expect(TokenType.RPAREN)
            return SubCall(className,subroutineName,[])

        exprList = []
        exprList.append(self.chop_expression())
        while self.peek().type is TokenType.COMMA:
            self.expect(TokenType.COMMA)
            exprList.append(self.chop_expression())
        self.expect(TokenType.RPAREN)
        return SubCall(className,subroutineName,exprList)

    def chop_parenthetical(self):
        self.expect(TokenType.LPAREN)
        expr = self.chop_expression()
        self.expect(TokenType.RPAREN)
        return expr

    def chop_term(self):
        match self.peek().type:
            case TokenType.INTLIT:
                return LitTerm(self.chop())
            case TokenType.STRLIT:
                return LitTerm(self.chop())
            case TokenType.KEYWORD:
                return LitTerm(self.chop())
            case TokenType.IDENT:
                if self.peek(1).type is TokenType.LBRACK:
                    return self.chop_subscript()
                if self.peek(1).type is TokenType.LPAREN or self.peek(1).type is TokenType.DOT:
                    return self.chop_subroutine()
                return LitTerm(self.chop())
            case TokenType.LPAREN:
                return self.chop_parenthetical()
    
    def chop_class(self):
        self.expect(TokenType.CLASS)
        className = self.expect(TokenType.IDENT)
        self.expect(TokenType.LBRACE)
        varDecList = []
        subroutineDecList = []
        while self.peek().type in (TokenType.STATIC,TokenType.FIELD):
            varDecList.append(self.chop_classVarDec())
        while self.peek().type is not TokenType.RBRACE:
            subroutineDecList.append(self.chop_subroutineDec())
        self.expect(TokenType.RBRACE)
        return JClass(className,varDecList,subroutineDecList)

    def chop_classVarDec(self):
        scope = self.expect(TokenType.STATIC,TokenType.FIELD)
        datatype = self.expect(*VarDatatypes)
        varnames = [self.expect(TokenType.IDENT)]
        while self.peek().type is TokenType.COMMA:
            self.expect(TokenType.COMMA)
            varnames.append(self.expect(TokenType.IDENT))
        self.expect(TokenType.SEMIC)
        return ClassVarDec(scope,datatype,varnames)

    def chop_subroutineDec(self):
        funcType = self.expect(TokenType.CONSTR,TokenType.FUNC,TokenType.METH)
        datatype = self.expect(*SubroutineDatatypes)
        subroutineName = self.expect(TokenType.IDENT)
        parameterList = []
        self.expect(TokenType.LPAREN)

        if self.peek().type in VarDatatypes:
            parameterList.append(Parameter(self.expect(*VarDatatypes),self.expect(TokenType.IDENT)))
            while self.peek().type is TokenType.COMMA:
                self.expect(TokenType.COMMA)
                parameterList.append(Parameter(self.expect(*VarDatatypes),self.expect(TokenType.IDENT)))
        self.expect(TokenType.RPAREN)

        subroutineBody = self.chop_subroutineBody()
        
        return SubroutineDec(funcType,datatype,subroutineName,parameterList,subroutineBody)
    
    def chop_subroutineBody(self):
        self.expect(TokenType.LBRACE)
        varDecList = []
        statementList = []
        while self.peek().type is TokenType.VAR:
            varDecList.append(self.chop_varDec())
        while self.peek().type is not TokenType.RBRACE:
            statementList.append(self.chop_statement())
        self.expect(TokenType.RBRACE)
        return SubroutineBody(varDecList,statementList)

    def chop_varDec(self):
        self.expect(TokenType.VAR)
        datatype = self.expect(*VarDatatypes)
        varnames = [self.expect(TokenType.IDENT)]
        while self.peek().type is TokenType.COMMA:
            self.expect(TokenType.COMMA)
            varnames.append(self.expect(TokenType.IDENT))
        self.expect(TokenType.SEMIC)
        return VarDec(datatype,varnames)


    def chop_statement(self):
        match self.peek().type:
            case TokenType.LET:
                return self.chop_letStatement()
            case TokenType.RETURN:
                return self.chop_returnStatement()
    
    def chop_letStatement(self):
        self.expect(TokenType.LET)
        varName = self.expect(TokenType.IDENT)
        index = None
        if self.peek().type is TokenType.LBRACK:
            self.expect(TokenType.LBRACK)
            index = self.chop_expression()
            self.expect(TokenType.RBRACK)
        self.expect(TokenType.EQUAL)
        expr = self.chop_expression()
        self.expect(TokenType.SEMIC)
        if index is None:
            return LetStatement(varName,expr)
        else:
            return SubscriptLetStatement(varName,index,expr)
    
    def chop_returnStatement(self):
        self.expect(TokenType.RETURN)
        expr = None
        if self.peek().type is not TokenType.SEMIC:
            expr = self.chop_expression()
        self.expect(TokenType.SEMIC)
        return ReturnStatement(expr)


        
