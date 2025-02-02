from memory import *
from sys import argv

def AND(a,b):
    r = ""
    if len(a) != 16 or len(b) != 16:
        raise Exception("Expect 16 bit values")
    for i in range(0,16):
        r = "1" if (a[i]=="1" and a[i]=="1") else "0"
    return r

def OR(a,b):
    astr = "{:016b}".format(a)
    bstr = "{:016b}".format(b)
    r = ""
    for i in range(0,16):
        r = "1" if astr[i]=="1" or bstr[i]=="1" else "0"
    return int(r,2)

if len(argv) < 2:
    exit()

code = []

with open(argv[1]) as f:
    for line in f:
        if line[0] == "#":
            continue
        code.append(line.strip())

ROM = CodeMemory(code)
RAM = Memory()

PC = 0
A = 0
D = 0

while PC != 30000:
    inst = ROM[PC]
    jumped = False
    match inst[0]:
        case "0":
            # A instruction
            A = int(inst[1:16],2)
        case "1":
            comp = inst[3:10]
            comp_val = None
            dest = inst[10:13]
            jump = inst[13:16]
            jumped = False
            match comp:
                case "0101010":
                    comp_val = 0
                case "0111111":
                    comp_val = 1
                case "0111010":
                    comp_val = -1
                case "0001100":
                    comp_val = D
                case "0110000":
                    comp_val = A
                case "1110000":
                    comp_val = RAM[A] # M
                case "0001101":
                    comp_val = 0b1111111111111111-D
                case "0110001":
                    comp_val = 0b1111111111111111-A
                case "1110001":
                    comp_val = 0b1111111111111111-RAM[A]
                case "0001111":
                    comp_val = 0-D
                case "0110011":
                    comp_val = 0-A
                case "1110011":
                    comp_val = 0-RAM[A]
                case "0011111":
                    comp_val = D+1
                case "0110111":
                    comp_val = A+1
                case "1110111":
                    comp_val = RAM[A]+1
                case "0001110":
                    comp_val = D-1
                case "0110010":
                    comp_val = A-1
                case "1110010":
                    comp_val = RAM[A]-1
                case "0000010":
                    comp_val = D+A
                case "1000010":
                    comp_val = D+RAM[A]
                case "0010011":
                    comp_val = D-A
                case "1010011":
                    comp_val = D-RAM[A]
                case "0000111":
                    comp_val = A-D
                case "1000111":
                    comp_val = RAM[A]-D
                case "0000000":
                    comp_val = AND(D,A)
                case "1000000":
                    comp_val = AND(D,RAM[A])
                case "0010101":
                    comp_val = OR(D,A)
                case "1010101":
                    comp_val = OR(D,RAM[A])
                case _:
                    raise Exception("Unrecognized opcode")
            match dest:
                case "001":
                    RAM[A] = comp_val
                case "010":
                    D = comp_val
                case "011":
                    RAM[A] = comp_val
                    D = comp_val
                case "100":
                    A = comp_val
                case "101":
                    RAM[A] = comp_val
                    A = comp_val
                case "110":
                    A = comp_val
                    D = comp_val
                case "111":
                    RAM[A] = comp_val
                    A = comp_val
                    D = comp_val
            match jump:
                case "001":
                    if comp_val > 0:
                        PC = A
                        jumped = True
                case "010":
                    if comp_val == 0:
                        PC = A
                        jumped = True
                case "011":
                    if comp_val >= 0:
                        PC = A
                        jumped = True
                case "100":
                    if comp_val < 0:
                        PC = A
                        jumped = True
                case "101":
                    if comp_val != 0:
                        PC = A
                        jumped = True
                case "110":
                    if comp_val <= 0:
                        PC = A
                        jumped = True
                case "111":
                    PC = A
                    jumped = True
    if not jumped:
        PC += 1
