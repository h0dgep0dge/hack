from glob import glob
from sys import argv
from jlexer import JLexer
from jparser import JParser
from jparser import *

class Compiler:

    def __init__(self,filename):
        self.filename = filename
        self.output = '.'.join(filename.split('.')[:-1])+'.vm'

        self.readfile()
        self.lex()
        self.parse()

    def readfile(self):
        self.source = ""
        f = open(self.filename)
        for line in f:
            self.source += line
    
    def lex(self):
        lexer = JLexer(self.source)
        self.tokens = []
        token = lexer.next_token()
        while token is not None:
            self.tokens.append(token)
            token = lexer.next_token()
    
    def parse(self):
        parser = JParser(self.tokens)
        parser.jclass()



if __name__ == "__main__":
    if len(argv) < 2:
        raise Exception("No folder specified")

    try:
        files = glob(argv[1] + "/*.jack")
    except Exception as error:
        print(error)
        exit()

    for file in files:
        c = Compiler(file)
