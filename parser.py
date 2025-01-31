from lexer import Token

class AInst:
    def __init__(self,value,tokens):
        self.type = "A"
        self.value = value
        self.tokens = tokens

    def gencode(self):
        return "0" + "{0:015b}".format(int(self.value.value))

class CInst:
    DEST_NULL = {"binary":"000","mne":"NULL"}
    DEST_M =    {"binary":"001","mne":"M"}
    DEST_D =    {"binary":"010","mne":"D"}
    DEST_MD =   {"binary":"011","mne":"MD"}
    DEST_A =    {"binary":"100","mne":"A"}
    DEST_AM =   {"binary":"101","mne":"AM"}
    DEST_AD =   {"binary":"110","mne":"AD"}
    DEST_AMD =  {"binary":"111","mne":"AMD"}

    COMP_ZERO =      {"binary":"0101010","mne":"0"}
    COMP_ONE =       {"binary":"0111111","mne":"1"}
    COMP_NEGONE =    {"binary":"0111010","mne":"-1"}
    COMP_D =         {"binary":"0001100","mne":"D"}
    COMP_A =         {"binary":"0110000","mne":"A"}
    COMP_M =         {"binary":"1110000","mne":"M"}
    COMP_NOTD =      {"binary":"0001101","mne":"!D"}
    COMP_NOTA =      {"binary":"0110001","mne":"!A"}
    COMP_NOTM =      {"binary":"1110001","mne":"!M"}
    COMP_NEGD =      {"binary":"0001111","mne":"-D"}
    COMP_NEGA =      {"binary":"0110011","mne":"-A"}
    COMP_NEGM =      {"binary":"1110011","mne":"-M"}
    COMP_DPLUSONE =  {"binary":"0011111","mne":"D+1"}
    COMP_APLUSONE =  {"binary":"0110111","mne":"A+1"}
    COMP_MPLUSONE =  {"binary":"1110111","mne":"M+1"}
    COMP_DMINUSONE = {"binary":"0001110","mne":"D-1"}
    COMP_AMINUSONE = {"binary":"0110010","mne":"A-1"}
    COMP_MMINUSONE = {"binary":"1110010","mne":"M-1"}
    COMP_DPLUSA =    {"binary":"0000010","mne":"D+A"}
    COMP_DPLUSM =    {"binary":"1000010","mne":"D+M"}
    COMP_DMINUSA =   {"binary":"0010011","mne":"D-A"}
    COMP_DMINUSM =   {"binary":"1010011","mne":"D-M"}
    COMP_AMINUSD =   {"binary":"0000111","mne":"A-D"}
    COMP_MMINUSD =   {"binary":"1000111","mne":"M-D"}
    COMP_DANDA =     {"binary":"0000000","mne":"D&A"}
    COMP_DANDM =     {"binary":"1000000","mne":"D&M"}
    COMP_DORA =      {"binary":"0010101","mne":"D|A"}
    COMP_DORM =      {"binary":"1010101","mne":"D|M"}

    JUMP_NULL = {"binary":"000","mne":"NULL"}
    JUMP_JGT = {"binary":"001","mne":"JGT"}
    JUMP_JEQ = {"binary":"010","mne":"JEQ"}
    JUMP_JGE = {"binary":"011","mne":"JGE"}
    JUMP_JLT = {"binary":"100","mne":"JLT"}
    JUMP_JNE = {"binary":"101","mne":"JNE"}
    JUMP_JLE = {"binary":"110","mne":"JLE"}
    JUMP_JMP = {"binary":"111","mne":"JMP"}

    def __init__(self,dest,comp,jump,tokens):
        self.type = "C"
        self.dest = dest
        self.comp = comp
        self.jump = jump
        self.tokens = tokens
    
    def gencode(self):
        return "111" + self.comp["binary"] + self.dest["binary"] + self.jump["binary"]

class Label:
    def __init__(self,label,tokens):
        self.type = "L"
        self.label = label
        self.tokens = tokens

class Parser:
    def __init__(self,tokens):
        self.ptr = 0
        self.tokens = tokens

    def remaining(self):
        return len(self.tokens) - self.ptr

    def peek(self,dist=0):
        if dist is None:
            return None if self.is_empty() else self.tokens[self.ptr]
        else:
            return None if self.remaining() <= dist else self.tokens[self.ptr+dist]
        
    
    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
        return r

    def is_empty(self):
        return self.remaining() <= 0

    def is_not_empty(self):
        return not self.is_empty()

    def make_unary(self):
        op = self.chop()
        if self.peek().type != Token.NAME and self.peek().type != Token.NUMBER:
            raise Exception("Unexpected token",self.peek())
        right = self.chop()
        return CInst.COMP_NOTA

    def make_plus(self,left,right):
        if right.value == "1":
            match left.value:
                case "A":
                    return CInst.COMP_APLUSONE
                case "M":
                    return CInst.COMP_MPLUSONE
                case "D":
                    return CInst.COMP_DPLUSA
                case "_":
                    print("Invalid addition operand",left)
        if left.value != "D":
            print("Invalid addition operand",left)
            return None
        match right.value:
            case "A":
                return CInst.COMP_DPLUSA
            case "M":
                return CInst.COMP_DPLUSM
            case _:
                print("Invalid addition operand",left)
                return None

    def make_minus(self,left,right):
        print(left,"-",right)
        match left.value:
            case "A":
                match right.value:
                    case "1":
                        return CInst.COMP_AMINUS1
                    case "A":
                        return CInst.COMP_AMINUSA
                    case "M":
                        return CInst.COMP_AMINUSM
                    case "D":
                        return CInst.COMP_AMINUSD
                    case _:
                        print("Invalid subtraction operand",right)
                        return None
            case "M":
                match right.value:
                    case "1":
                        return CInst.COMP_MMINUS1
                    case "A":
                        return CInst.COMP_MMINUSA
                    case "M":
                        return CInst.COMP_MMINUSM
                    case "D":
                        return CInst.COMP_MMINUSD
                    case _:
                        print("Invalid subtraction operand",right)
                        return None
            case "D":
                match right.value:
                    case "1":
                        return CInst.COMP_DMINUS1
                    case "A":
                        return CInst.COMP_DMINUSA
                    case "M":
                        return CInst.COMP_DMINUSM
                    case "D":
                        return CInst.COMP_DMINUSD
                    case _:
                        print("Invalid subtraction operand",right)
                        return None
            case _:
                print("Invalid subtraction operand",left)
                return None

    def make_or(self,left,right):
        if left.value != "D":
            print("Invalid OR operand",left)
            return None
        match right.value:
            case "A":
                return CInst.COMP_DORA
            case "M":
                return CInst.COMP_DORM
    
    def make_and(self,left,right):
        if left.value != "D":
            print("Invalid AND operand",left)
            return None
        match right.value:
            case "A":
                return CInst.COMP_DANDA
            case "M":
                return CInst.COMP_DANDM


    def make_comp(self):
        if self.peek().type == Token.MINUS or self.peek().type == Token.EXCLAM:
            return self.make_unary()
        if self.peek().type != Token.NAME and self.peek().type != Token.NUMBER:
            raise Exception("Unexpected token",self.peek())
        left = self.chop()
        if self.is_empty() or (self.peek().type != Token.PLUS and self.peek().type != Token.MINUS and self.peek().type != Token.AMPER and self.peek().type != Token.PIPE):
            match left.value:
                case "A":
                    return CInst.COMP_A
                case "M":
                    return CInst.COMP_M
                case "D":
                    return CInst.COMP_D
                case "0":
                    return CInst.COMP_ZERO
                case "1":
                    return CInst.COMP_ONE
        oper = self.chop()
        if self.peek().type != Token.NUMBER and self.peek().type != Token.NAME:
            raise Exception("Unexpected token",self.peek())
        right = self.chop()
        match oper.type:
            case Token.PLUS:
                return self.make_plus(left,right)
            case Token.MINUS:
                return self.make_minus(left,right)
            case Token.AMPER:
                return self.make_and(left,right)
            case Token.PIPE:
                return self.make_or(left,right)
        print("Invalid operator",oper)
        return None

    def make_c_instruction(self):
        start = self.ptr
        dest = None
        comp = None
        jump = None
        if self.peek(1).type == Token.EQUAL:
            if self.peek().type != Token.NAME:
                raise Exception("Unexpected token",self.peek())
            match self.chop().value:
                case "D":
                    dest = CInst.DEST_D
                case "M":
                    dest = CInst.DEST_M
                case "MD":
                    dest = CInst.DEST_MD
                case "A":
                    dest = CInst.DEST_A
                case "AD":
                    dest = CInst.DEST_AD
                case "AM":
                    dest = CInst.DEST_AM
                case "AMD":
                    dest = CInst.DEST_AMD
                case "_":
                    print("Invalid dest spec",self.peek(-1))
                    return None
            self.chop()
        else:
            dest = CInst.DEST_NULL
        
        comp = self.make_comp()
        if comp == None:
            return None

        if self.is_not_empty() and self.peek().type == Token.SEMICO:
            self.chop()
            if self.peek().type != Token.NAME:
                raise Exception("Unexpected token",self.peek())
            match self.chop().value:
                case "JGT":
                    jump = CInst.JUMP_JGT
                case "JEQ":
                    jump = CInst.JUMP_JEQ
                case "JGE":
                    jump = CInst.JUMP_JGE
                case "JLT":
                    jump = CInst.JUMP_JLT
                case "JNE":
                    jump = CInst.JUMP_JNE
                case "JLE":
                    jump = CInst.JUMP_JLE
                case "JMP":
                    jump = CInst.JUMP_JMP
                case _:
                    print("Invalid jump spec",self.peek(-1))
        else:
            jump = CInst.JUMP_NULL
        return CInst(dest,comp,jump,self.tokens[start:self.ptr])

    def make_a_instruction(self):
        start = self.ptr
        self.chop()
        v = self.chop()
        if v.type != Token.NAME and v.type != Token.NUMBER:
            raise Exception("Unexpected token",v)
        return AInst(v,self.tokens[start:self.ptr])

    def make_label(self):
        start = self.ptr
        self.chop()
        if self.peek().type != Token.NAME:
            raise Exception("Unexpected token",self.peek())
        label = self.chop()
        if self.peek().type != Token.RPAREN:
            raise Exception("Unexpected token",self.peek())
        self.chop()
        return Label(label,self.tokens[start:self.ptr])

    def next_instruction(self):
        if self.is_empty():
            return None
        match self.peek().type:
            case Token.AT:
                return self.make_a_instruction()
            case Token.LPAREN:
                return self.make_label()
            case _:
                return self.make_c_instruction()
