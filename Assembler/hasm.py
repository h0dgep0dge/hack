from lexer import Lexer
from parser import Parser
from dereferencer import Dereferencer
from sys import argv

if len(argv) < 2:
    exit()

sourcefile = argv[1]
binaryfile = argv[1]+".hack"

source = ""
with open(argv[1]) as f:
    for line in f:
        source += line

lex = Lexer(source)
tokens = []

try:
    token = lex.next_token()
    while token is not None:
        tokens.append(token)
        token = lex.next_token()
except Exception as error:
    print(error)

parse = Parser(tokens)
instructions = []

try:
    inst = parse.next_instruction()
    while inst is not None:
        instructions.append(inst)
        inst = parse.next_instruction()
except Exception as error:
    print(error.args[0],error.args[1])

deref = Dereferencer(instructions)
deref.create_label_references()
deref.create_variable_references()
derefed = deref.dereference()

with open(binaryfile, "w") as binary:
    for inst in derefed:
        binary.write(inst.gencode()+"\n")
