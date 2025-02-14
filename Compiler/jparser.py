from jlexer import TokenType
from progclasses import *

BinaryOperators = [TokenType.PLUS,  TokenType.MINUS, TokenType.STAR,
                   TokenType.SLASH, TokenType.AMPER, TokenType.PIPE,
                   TokenType.LTHAN, TokenType.GTHAN, TokenType.EQUAL]
UnaryOperators = [TokenType.MINUS,TokenType.TILDE]

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
            return None
        return self.tokens[self.ptr+offset]

    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
            if r == "\n":
                self.line += 1
        return r

    def expect(self,tokentype):
        if self.is_not_empty() and self.peek().type == tokentype:
            return self.chop()
        if self.is_empty():
            raise Exception("Unexpected end of file")
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
                if self.peek(1).type is TokenType.LPAREN:
                    return self.chop_subroutine()
                return LitTerm(self.chop())
            case TokenType.LPAREN:
                return self.chop_parenthetical()
