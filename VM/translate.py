from lexer import VMLexer
from parser import VMParser
from codegen import VMCodeGen
import sys

if len(sys.argv) <= 1:
    print("No input file")
    exit()

sourcefile = sys.argv[1]
source = ""

try:
    with open(sourcefile) as f:
        for line in f:
            source += line
except FileNotFoundError:
    print("Source file not found",sourcefile)

lex = VMLexer(source)
tokens = []

token = lex.next_token()
while token is not None:
    tokens.append(token)
    token = lex.next_token()

parse = VMParser(tokens)
instructions = []

gen = VMCodeGen(sourcefile)

print(
"""
@256
D=A
@SP
M=D

@1017
D=A
@LCL
M=D
""")

instr = parse.next_instruction()
while instr is not None:
    print(gen.gen(instr))
    #print(instr)
    instr = parse.next_instruction()

print(
"""
(HALT)
@HALT
0;JMP
"""
)