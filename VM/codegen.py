from parser import OperationTypes,Operation,Push

class VMCodeGen:
    def __init__(self):
        self.labelCounter = 0
    
    def gen_push(self,instr):
        match instr.segment:
            case "constant":
                return """
@{index}
D=A
@SP
A=M
M=D
@SP
M=M+1""".format(index=instr.index)
            case _:
                raise Exception("Segment not implemented",instr.segment)
    
    def gen_operation(self,instr):
        match instr.type:
            case OperationTypes.ADD:
                return """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1
"""
            case _:
                raise Exception("Not implemented")

    def gen(self,instr):
        if type(instr) is Push:
            return self.gen_push(instr)
        if type(instr) is Operation:
            return self.gen_operation(instr)