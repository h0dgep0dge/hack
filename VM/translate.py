from lexer import VMLexer
from parser import VMParser
from codegen import VMCodeGen
from glob import glob
from sys import argv
import os

class Translator:
    def __init__(self,filepath):
        self.filepath = filepath

        self.basename = os.path.basename(filepath)
        self.filename = ".".join(self.basename.split(".")[:-1])

        self.read()
        self.lex()
        self.parse()
        self.gen()
    
    def read(self):
        self.source = ""
        with open(self.filepath) as f:
            for line in f:
                self.source += line
    
    def lex(self):
        self.tokens = []
        lex = VMLexer(self.source)
        token = lex.next_token()
        while token is not None:
            self.tokens.append(token)
            token = lex.next_token()

    def parse(self):
        self.instructions = []
        parse = VMParser(self.tokens)
        instruction = parse.next_instruction()
        while instruction is not None:
            self.instructions.append(instruction)
            instruction = parse.next_instruction()

    def gen(self):
        self.code = ""
        gen = VMCodeGen(self.filename)
        for instr in self.instructions:
            self.code += f"// {instr} \n"
            self.code += gen.gen(instr)
        


if len(argv) < 2:
    raise Exception("No folder specified")

try:
    files = glob(argv[1] + "/*.vm")
except Exception as error:
    print(error)

output = argv[1] + "/" + os.path.basename(argv[1]) + ".hack"

f = open(output,"w")

f.write( # Bootstrap
"""
@256
D=A
@SP
M=D

@Sys.init
0;JMP

""")

for file in files:
    f.write(Translator(file).code)
