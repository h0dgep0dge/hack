from lexer import VMLexer
from parser import VMParser,VMInstruction,VMInstructionType
from codegen import VMCodeGen
import sys

class InstrList(list):
    def __repr__(self):
        r = ""
        newline = ""
        for item in self:
            r += newline + repr(item)
            newline = "\n"
        return r

if len(sys.argv) <= 1:
    print("No input file")
    exit()

sourcefile = sys.argv[1]
filename = ".".join(sourcefile.split(".")[:-1])
source = ""

try:
    with open(sourcefile) as f:
        for line in f:
            source += line
except FileNotFoundError:
    print("Source file not found",sourcefile)
    exit()

lex = VMLexer(source)
tokens = []

token = lex.next_token()
while token is not None:
    tokens.append(token)
    token = lex.next_token()

parse = VMParser(tokens)

instructions = InstrList([VMInstruction(VMInstructionType.CALL,"Main.main",0,None),VMInstruction(VMInstructionType.LABEL,"HALT",None,None),VMInstruction(VMInstructionType.GOTO,"HALT",None,None)])
#instructions = InstrList()
instr = parse.next_instruction()
while instr is not None:
    instructions.append(instr)
    instr = parse.next_instruction()

#print(instructions)
#exit()

gen = VMCodeGen(filename,instructions)

print(
"""
@256
D=A
@SP
M=D


""")
for instr in instructions:
    print("//",instr)
    print(gen.gen(instr))
