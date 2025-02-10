from parser import ArithType,VMInstructionType

class VMCodeGen:
    POPTOD = "@SP\nM=M-1\nA=M\nD=M\n"
    POINT = "@SP\nM=M-1\nA=M\n"
    INCREMENT = "@SP\nM=M+1\n"
    DECREMENT = "@SP\nM=M-1\n"
    PUSHD = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    PUSHA = "D=A\n" + PUSHD
    PUSHM = "D=M\n" + PUSHD

    def __init__(self,filename):
        self.filename = filename

        self.labelCounter = 0
        self.currentFunction = "default"

    def gen_function(self,instr): # FUNC = 6 arg1=name arg2=localc
        return f"({instr.arg1}) \n @0 \n D=A \n" + VMCodeGen.PUSHD * instr.arg2

    def gen_return(self,instr): # RETURN = 8 no arguments
        return f"{VMCodeGen.POPTOD} \n @13 \n M=D \n @ARG \n D=M \n @14 \n M=D \n @LCL \n D=M \n @SP \n M=D \n {VMCodeGen.POPTOD} \n @THAT \n M=D \n {VMCodeGen.POPTOD} \n @THIS \n M=D \n {VMCodeGen.POPTOD} \n @ARG \n M=D \n {VMCodeGen.POPTOD} \n @LCL \n M=D \n {VMCodeGen.POPTOD} \n @15 \n M=D \n @14 \n D=M \n @SP \n M=D \n @13 \n D=M \n {VMCodeGen.PUSHD} \n @15 \n A=M \n 0;JMP \n"

    def gen_call(self,instr): # CALL = 7 arg1=name arg2=argc
        label = self.new_return_label()
        return f"@{label} \n D=A \n {VMCodeGen.PUSHD} \n @LCL \n {VMCodeGen.PUSHM} \n @ARG \n {VMCodeGen.PUSHM} \n @THIS \n {VMCodeGen.PUSHM} \n @THAT \n {VMCodeGen.PUSHM} \n @{instr.arg2 + 5} \n D=A \n @SP \n D=M-D \n @ARG \n M=D \n @SP \n D=M \n @LCL \n M=D \n @{instr.arg1} \n 0;JMP \n ({label}) \n"
    
    def new_label(self):
        self.labelCounter += 1
        return f"{self.currentFunction}$" + str(self.labelCounter)
    
    def new_return_label(self):
        self.labelCounter += 1
        return f"{self.currentFunction}$ret.{self.labelCounter}"

    def gen_constant_push(self,value):
        return f"@{value} \n D=A \n" + VMCodeGen.PUSHD

    def gen_relative_push(self,segment,index):
        return f"@{segment}  \n D=M \n @{index} \n A=D+A \n D=M \n" + VMCodeGen.PUSHD

    def gen_absolute_push(self,addr):
        return f"@{addr} \n D=M \n" + VMCodeGen.PUSHD
    
    def gen_static_push(self,index):
        return f"@{self.filename}.{str(index)} \n D=M \n" + VMCodeGen.PUSHD

    def gen_relative_pop(self,segment,index):
        return f"@{segment} \n D=M \n @{index} \n D=D+A \n @13 \n M=D \n" + VMCodeGen.POPTOD + "@13 \n A=M \n M=D \n"

    def gen_absolute_pop(self,addr):
        return VMCodeGen.POPTOD + f"@{addr} \n M=D \n"
    
    def gen_static_pop(self,index):
        return VMCodeGen.POPTOD + f"@{self.filename}.{str(index)} \n M=D \n"
    
    def gen_push(self,instr): # PUSH = 1 arg1=segment arg2=index
        match instr.arg1:
            case "constant":
                return self.gen_constant_push(instr.arg2)
            case "local":
                return self.gen_relative_push("LCL",instr.arg2)
            case "argument":
                return self.gen_relative_push("ARG",instr.arg2)
            case "this":
                return self.gen_relative_push("THIS",instr.arg2)
            case "that":
                return self.gen_relative_push("THAT",instr.arg2)
            case "pointer":
                return self.gen_absolute_push(3+instr.arg2)
            case "temp":
                return self.gen_absolute_push(5+instr.arg2)
            case "static":
                return self.gen_static_push(instr.arg2)
            case _:
                raise Exception("Segment not implemented",instr.arg1)
    
    def gen_pop(self,instr): # POP = 0 arg1=segment arg2=index
        match instr.arg1:
            case "local":
                return self.gen_relative_pop("LCL",instr.arg2)
            case "argument":
                return self.gen_relative_pop("ARG",instr.arg2)
            case "this":
                return self.gen_relative_pop("THIS",instr.arg2)
            case "that":
                return self.gen_relative_pop("THAT",instr.arg2)
            case "pointer":
                return self.gen_absolute_pop(3+instr.arg2)
            case "temp":
                return self.gen_absolute_pop(5+instr.arg2)
            case "static":
                return self.gen_static_pop(instr.arg2)
            case _:
                raise Exception("Segment not implemented",instr.arg1)
    
    def gen_label(self,instr): # LABEL = 4 arg1=label
        return f"({self.currentFunction}${instr.arg1})\n"
    
    def gen_goto(self,instr): # GOTO = 2 arg1=label
        return f"@{self.currentFunction}${instr.arg1} \n 0;JMP \n"
    
    def gen_ifgoto(self,instr): # IFGOTO = 3 arg1=label
        return VMCodeGen.POPTOD + f"@{self.currentFunction}${instr.arg1} \n D;JNE \n"

    def gen_comparison(self,jump):
        trueLabel = self.new_label()
        falseLabel = self.new_label()
        contLabel = self.new_label()

        return VMCodeGen.POPTOD + VMCodeGen.POINT + f" D=M-D\n @{trueLabel} \n D;{jump} \n @{falseLabel} \n 0;JMP \n ({trueLabel}) \n @SP \n A=M \n M=0 \n M=!M \n @{contLabel} \n 0;JMP \n ({falseLabel}) \n @SP \n A=M \n M=0 \n ({contLabel}) \n" + VMCodeGen.INCREMENT

    def gen_arith(self,instr): # ARITH = 5 arg1=ArithType
        match instr.arg1:
            case ArithType.ADD:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D+M\n" + VMCodeGen.INCREMENT
            case ArithType.SUB:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=M-D\n" + VMCodeGen.INCREMENT
            case ArithType.AND:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D&M\n" + VMCodeGen.INCREMENT
            case ArithType.OR:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D|M\n" + VMCodeGen.INCREMENT
            case ArithType.NEG:
                return VMCodeGen.POINT + "M=-M\n" + VMCodeGen.INCREMENT
            case ArithType.NOT:
                return VMCodeGen.POINT + "M=!M\n" + VMCodeGen.INCREMENT
            case ArithType.EQ:
                return self.gen_comparison("JEQ")
            case ArithType.GT:
                return self.gen_comparison("JGT")
            case ArithType.LT:
                return self.gen_comparison("JLT")
            case _:
                raise Exception("Unknown ArithType",instr.arg1)

    def gen(self,instr):
        match instr.type:
            case VMInstructionType.PUSH:
                return self.gen_push(instr)
            case VMInstructionType.POP:
                return self.gen_pop(instr)
            case VMInstructionType.LABEL:
                return self.gen_label(instr)
            case VMInstructionType.GOTO:
                return self.gen_goto(instr)
            case VMInstructionType.IFGOTO:
                return self.gen_ifgoto(instr)
            case VMInstructionType.ARITH:
                return self.gen_arith(instr)
            case VMInstructionType.FUNC:
                self.currentFunction = instr.arg1
                return self.gen_function(instr)
            case VMInstructionType.RETURN:
                return self.gen_return(instr)
            case VMInstructionType.CALL:
                return self.gen_call(instr)
            case _:
                raise Exception("Instruction not implemented",instr)
