from parser import OperationTypes,Operation,Push

class VMCodeGen:
    POPTOD = "@SP\nM=M-1\nA=M\nD=M\n"
    POINT = "@SP\nM=M-1\nA=M\n"
    INCREMENT = "@SP\nM=M+1\n"

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
        return f"@{self.filename+"."+str(index)} \n D=M \n" + VMCodeGen.PUSHD

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
    
    def gen_comparison(self,jump):
        trueLabel = self.new_label()
        falseLabel = self.new_label()
        continueLabel = self.new_label()

        return VMCodeGen.POPTOD + VMCodeGen.POINT + " D=M-D\n @{true} \n D;{jump} \n @{false} \n 0;JMP \n ({true}) \n @SP \n A=M \n M=0 \n M=!M \n @{cont} \n 0;JMP \n ({false}) \n @SP \n A=M \n M=0 \n ({cont}) \n".format(true=trueLabel,false=falseLabel,cont=continueLabel,jump=jump) + VMCodeGen.INCREMENT

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
        if type(instr) is Operation:
            return self.gen_operation(instr)