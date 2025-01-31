from lexer import Lexer
from parser import Parser
from dereferencer import Dereferencer

source = ""
with open("fib.asm") as f:
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

for inst in derefed:
    #print(inst.gencode(),inst.tokens)
    print(inst.gencode())