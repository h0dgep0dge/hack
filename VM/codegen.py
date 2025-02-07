from parser import OperationTypes,Operation,Push,Pop,Label,Goto

class VMCodeGen:
    POPTOD = "@SP\nM=M-1\nA=M\nD=M\n"
    POINT = "@SP\nM=M-1\nA=M\n"
    INCREMENT = "@SP\nM=M+1\n"
    DECREMENT = "@SP\nM=M-1\n"

    PUSHD = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    def __init__(self,filename):
        self.filename = filename
        self.labelCounter = 0

    def new_label(self):
        self.labelCounter += 1
        return "VM$" + str(self.labelCounter)

    def gen_constant_push(self,value):
        return f"@{value} \n D=A \n" + VMCodeGen.PUSHD

    def gen_relative_push(self,segment,index):
        return f"@{segment} \n D=M \n @{index} \n A=D+A \n D=M \n" + VMCodeGen.PUSHD

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
    

    def gen_push(self,instr):
        match instr.segment:
            case "constant":
                return self.gen_constant_push(instr.index)
            case "local":
                return self.gen_relative_push("LCL",instr.index)
            case "argument":
                return self.gen_relative_push("ARG",instr.index)
            case "this":
                return self.gen_relative_push("THIS",instr.index)
            case "that":
                return self.gen_relative_push("THAT",instr.index)
            case "pointer":
                return self.gen_absolute_push(3+instr.index)
            case "temp":
                return self.gen_absolute_push(5+instr.index)
            case "static":
                return self.gen_static_push(instr.index)
            case _:
                raise Exception("Segment not implemented",instr.segment)
    
    def gen_pop(self,instr):
        match instr.segment:
            case "local":
                return self.gen_relative_pop("LCL",instr.index)
            case "argument":
                return self.gen_relative_pop("ARG",instr.index)
            case "this":
                return self.gen_relative_pop("THIS",instr.index)
            case "that":
                return self.gen_relative_pop("THAT",instr.index)
            case "pointer":
                return self.gen_absolute_pop(3+instr.index)
            case "temp":
                return self.gen_absolute_pop(5+instr.index)
            case "static":
                return self.gen_static_pop(instr.index)
            case _:
                raise Exception("Segment not implemented",instr.segment)
    
    def gen_label(self,instr):
        return f"({self.filename}.{instr.label})\n"
    
    def gen_goto(self,instr):
        if instr.cond:
            return VMCodeGen.POPTOD + f"@{self.filename}.{instr.label} \n D;JNE \n"
        return f"@{self.filename}.{instr.label} \n 0;JMP \n"

    def gen_comparison(self,jump):
        trueLabel = self.new_label()
        falseLabel = self.new_label()
        contLabel = self.new_label()

        return VMCodeGen.POPTOD + VMCodeGen.POINT + f" D=M-D\n @{trueLabel} \n D;{jump} \n @{falseLabel} \n 0;JMP \n ({trueLabel}) \n @SP \n A=M \n M=0 \n M=!M \n @{contLabel} \n 0;JMP \n ({falseLabel}) \n @SP \n A=M \n M=0 \n ({contLabel}) \n" + VMCodeGen.INCREMENT

    def gen_operation(self,instr):
        match instr.type:
            case OperationTypes.ADD:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D+M\n" + VMCodeGen.INCREMENT
            case OperationTypes.SUB:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=M-D\n" + VMCodeGen.INCREMENT
            case OperationTypes.AND:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D&M\n" + VMCodeGen.INCREMENT
            case OperationTypes.OR:
                return VMCodeGen.POPTOD + VMCodeGen.POINT + "M=D|M\n" + VMCodeGen.INCREMENT
            case OperationTypes.NEG:
                return VMCodeGen.POINT + "M=-M\n" + VMCodeGen.INCREMENT
            case OperationTypes.NOT:
                return VMCodeGen.POINT + "M=!M\n" + VMCodeGen.INCREMENT
            case OperationTypes.EQ:
                return self.gen_comparison("JEQ")
            case OperationTypes.GT:
                return self.gen_comparison("JGT")
            case OperationTypes.LT:
                return self.gen_comparison("JLT")
            case _:
                raise Exception("Not implemented")

    def gen(self,instr):
        if type(instr) is Push:
            return self.gen_push(instr)
        elif type(instr) is Pop:
            return self.gen_pop(instr)
        elif type(instr) is Goto:
            return self.gen_goto(instr)
        elif type(instr) is Label:
            return self.gen_label(instr)
        elif type(instr) is Operation:
            return self.gen_operation(instr)