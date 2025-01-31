from lexer import Token
from parser import AInst

class Dereferencer:
    def __init__(self,instructions):
        self.instructions = instructions
        self.ptr = 0
        self.table = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"R0": 0,"R1": 1,"R2": 2,"R3": 3,"R4": 4,"R5": 5,"R6": 6,"R7": 7,"R8": 8,"R9": 9,"R10": 10,"R11": 11,"R12": 12,"R13": 13,"R14": 14,"R15": 15,"SCREEN": 16384,"KBD": 24576}
        self.var_index = 16
    
    def symbol_exists(self,symbol):
        return symbol in self.table

    def allocate_var(self,symbol):
        if self.symbol_exists(symbol):
            raise Exception("Variable already allocated",symbol)
        self.table[symbol] = self.var_index
        self.var_index += 1

    def create_label(self,symbol,index):
        if self.symbol_exists(symbol):
            raise Exception("Label already exists",symbol)
        self.table[symbol] = index
    
    def dereference_symbol(self,symbol):
        if not self.symbol_exists(symbol):
            raise Exception("Symbol doesn't exist",symbol)
        return self.table[symbol]

    def create_label_references(self):
        index = 0
        instruction = 0
        while index < len(self.instructions):
            inst = self.instructions[index]
            if inst.type == "L":
                if self.symbol_exists(inst.label.value):
                    raise Exception("Label already exists",inst.label.value)
                self.create_label(inst.label.value,instruction)
            else:
                instruction += 1
            index += 1
    
    def create_variable_references(self):
        index = 0
        while index < len(self.instructions):
            inst = self.instructions[index]
            if inst.type == "A" and inst.value.type == Token.NAME and not self.symbol_exists(inst.value.value):
                self.allocate_var(inst.value.value)
            index += 1
    
    def dereference(self):
        derefed = []
        index = 0
        while index < len(self.instructions):
            inst = self.instructions[index]
            match inst.type:
                case "A":
                    if inst.value.type == Token.NAME:
                        derefed.append(AInst(
                            Token(Token.NUMBER,str(self.dereference_symbol(inst.value.value)),inst.value.line)
                        ,inst.tokens))
                    else:
                        derefed.append(inst)
                case "C":
                    derefed.append(inst)
            index += 1
        return derefed
                




