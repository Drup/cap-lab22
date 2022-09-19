from antlr4 import InputStream
from antlr4 import CommonTokenStream

# include to use the generated lexer and parser
from ITELexer import ITELexer
from ITEParser import ITEParser

import sys


def main():
    lexer = ITELexer(InputStream(sys.stdin.read()))
    stream = CommonTokenStream(lexer)
    parser = ITEParser(stream)
    parser.prog()
    print("Finished")


# warns pb if py file is included in others
if __name__ == '__main__':
    main()
