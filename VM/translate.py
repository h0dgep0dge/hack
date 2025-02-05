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

gen = VMCodeGen()

print(
"""
@SP
M=100
""")

instr = parse.next_instruction()
while instr is not None:
    print(gen.gen(instr))
    instr = parse.next_instruction()

