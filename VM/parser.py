from lexer import TokenType
from enum import Enum



class PushPop:
    def __init__(self,segment,index,tokens):
        self.segment = segment
        self.index = index
        self.tokens = tokens

class Push(PushPop):
    def __repr__(self):
        return "Push( \"" + self.segment + "\" , " + str(self.index) + " )"

class Pop(PushPop):
    def __repr__(self):
        return "Pop( \"" + self.segment + "\" , " + str(self.index) + " )"

class Label:
    def __init__(self,label,tokens):
        self.label = label
        self.tokens = tokens

    def __repr__(self):
        return "Label( " + self.label + " )"

class Goto:
    def __init__(self,label,cond,tokens):
        self.label = label
        self.tokens = tokens
        self.cond = cond
    
    def __repr__(self):
        return "Goto( " + self.label + " , cond=" + str(self.cond) + " )"

class OperationTypes(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ = 3
    GT = 4
    LT = 5
    AND = 6
    OR = 7
    NOT = 8

class Operation:
    def __init__(self,type,tokens):
        self.type = type
        self.tokens = tokens
    
    def __repr__(self):
        return "Operation( " + self.type.name + " )"


class VMParser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.ptr = 0
    
    def is_empty(self):
        return self.ptr >= len(self.tokens)

    def is_not_empty(self):
        return not self.is_empty()

    def peek(self):
        if self.is_empty():
            return None
        return self.tokens[self.ptr]
    
    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
        return r

    def chop_push(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        segment = self.expect(TokenType.IDENT,chop=True)
        index = self.expect(TokenType.NUMBER,chop=True)
        return Push(segment.source,int(index.source),self.tokens[start:self.ptr])

    def chop_pop(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        segment = self.expect(TokenType.IDENT,chop=True)
        index = self.expect(TokenType.NUMBER,chop=True)
        return Pop(segment.source,int(index.source),self.tokens[start:self.ptr])

    def chop_label(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        label = self.expect(TokenType.IDENT,chop=True)
        return Label(label.source,self.tokens[start:self.ptr])

    def chop_goto(self,cond=False):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        label = self.expect(TokenType.IDENT,chop=True)
        return Goto(label.source,cond,self.tokens[start:self.ptr])


    def chop_op(self,type):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        return Operation(type,self.tokens[start:self.ptr])


    def expect(self,tokentype,chop=False):
        if self.is_empty():
            raise Exception("Unexpected end of file")
        r = self.peek()
        if r.type != tokentype:
            raise Exception("Unexpected token",self.peek())
        if chop:
            self.chop()
        return r

    def next_instruction(self):
        
        while self.is_not_empty() and self.peek().type == TokenType.NEWLINE:
            self.chop()

        if self.is_empty():
            return None
        
        match self.expect(TokenType.IDENT).source:
            case "push":
                r = self.chop_push()
            case "pop":
                r = self.chop_pop()
            case "label":
                r = self.chop_label()
            case "goto":
                r = self.chop_goto()
            case "if-goto":
                r = self.chop_goto(cond=True)
            case "add":
                r = self.chop_op(OperationTypes.ADD)
            case "sub":
                r = self.chop_op(OperationTypes.SUB)
            case "neg":
                r = self.chop_op(OperationTypes.NEG)
            case "eq":
                r = self.chop_op(OperationTypes.EQ)
            case "gt":
                r = self.chop_op(OperationTypes.GT)
            case "lt":
                r = self.chop_op(OperationTypes.LT)
            case "and":
                r = self.chop_op(OperationTypes.AND)
            case "or":
                r = self.chop_op(OperationTypes.OR)
            case "not":
                r = self.chop_op(OperationTypes.NOT)
            case _:
                raise Exception("Unexpected token",self.tokens[self.ptr])
        
        if self.is_not_empty():
            self.expect(TokenType.NEWLINE,chop=True)
        return r
