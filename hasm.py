from lexer import Lexer
from parser import Parser

source = ""
with open("fibNL.asm") as f:
    for line in f:
        source += line

lex = Lexer(source)
tokens = []

token = lex.next_token()
while token is not None:
    tokens.append(token)
    #print(token)
    token = lex.next_token()

parse = Parser(tokens)

inst = parse.next_instruction()
while inst is not None:
    match inst.type:
        case "A":
            print(inst.value.line,"@",inst.value.value)
        case "C":
            print(inst.tokens[0].line,inst.dest["mne"],"=",inst.comp["mne"],";",inst.jump["mne"])
    inst = parse.next_instruction()
    