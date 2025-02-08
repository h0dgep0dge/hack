from lexer import TokenType
from enum import Enum

class ArithType(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ = 3
    GT = 4
    LT = 5
    AND = 6
    OR = 7
    NOT = 8

class VMInstructionType(Enum):
    POP = 0 # arg1=segment arg2=index
    PUSH = 1 # arg1=segment arg2=index
    GOTO = 2 # arg1=label
    IFGOTO = 3 # arg1=label
    LABEL = 4 # arg1=label
    ARITH = 5 # arg1=ArithType
    FUNC = 6 # arg1=name arg2=argc
    CALL = 7 # arg1=name arg2=argc
    RETURN = 8 # no arguments

class VMInstruction:
    def __init__(self,type,arg1,arg2,tokens):
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2
        self.tokens = tokens
    
    def __repr__(self):
        #return f"VMInstruction( {self.type.name} , {repr(self.arg1)} , {repr(self.arg2)} , {self.tokens} )"
        return f"VMInstruction( {self.type.name} , {repr(self.arg1)} , {repr(self.arg2)} )"

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
        return VMInstruction(VMInstructionType.PUSH,segment.source,int(index.source),self.tokens[start:self.ptr])

    def chop_pop(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        segment = self.expect(TokenType.IDENT,chop=True)
        index = self.expect(TokenType.NUMBER,chop=True)
        return VMInstruction(VMInstructionType.POP,segment.source,int(index.source),self.tokens[start:self.ptr])

    def chop_func(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        name = self.expect(TokenType.IDENT,chop=True)
        argc = self.expect(TokenType.NUMBER,chop=True)
        return VMInstruction(VMInstructionType.FUNC,name.source,int(argc.source),self.tokens[start:self.ptr])

    def chop_call(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        name = self.expect(TokenType.IDENT,chop=True)
        argc = self.expect(TokenType.NUMBER,chop=True)
        return VMInstruction(VMInstructionType.CALL,name.source,int(argc.source),self.tokens[start:self.ptr])

    def chop_return(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        return VMInstruction(VMInstructionType.RETURN,None,None,self.tokens[start:self.ptr])

    def chop_label(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        label = self.expect(TokenType.IDENT,chop=True)
        return VMInstruction(VMInstructionType.LABEL,label.source,None,self.tokens[start:self.ptr])

    def chop_goto(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        label = self.expect(TokenType.IDENT,chop=True)
        return VMInstruction(VMInstructionType.GOTO,label.source,None,self.tokens[start:self.ptr])

    def chop_ifgoto(self):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        label = self.expect(TokenType.IDENT,chop=True)
        return VMInstruction(VMInstructionType.IFGOTO,label.source,None,self.tokens[start:self.ptr])


    def chop_arith(self,type):
        start = self.ptr
        self.expect(TokenType.IDENT,chop=True)
        return VMInstruction(VMInstructionType.ARITH,type,None,self.tokens[start:self.ptr])


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
                r = self.chop_ifgoto()
            case "function":
                r = self.chop_func()
            case "call":
                r = self.chop_call()
            case "return":
                r = self.chop_return()
            case "add":
                r = self.chop_arith(ArithType.ADD)
            case "sub":
                r = self.chop_arith(ArithType.SUB)
            case "neg":
                r = self.chop_arith(ArithType.NEG)
            case "eq":
                r = self.chop_arith(ArithType.EQ)
            case "gt":
                r = self.chop_arith(ArithType.GT)
            case "lt":
                r = self.chop_arith(ArithType.LT)
            case "and":
                r = self.chop_arith(ArithType.AND)
            case "or":
                r = self.chop_arith(ArithType.OR)
            case "not":
                r = self.chop_arith(ArithType.NOT)
            case _:
                raise Exception("Unexpected token",self.tokens[self.ptr])
        
        if self.is_not_empty():
            self.expect(TokenType.NEWLINE,chop=True)
        return r
