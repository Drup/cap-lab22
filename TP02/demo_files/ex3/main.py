from antlr4 import InputStream
from antlr4 import CommonTokenStream

# include to use the generated lexer and parser
from Example3Lexer import Example3Lexer
from Example3Parser import Example3Parser

import sys


def main():
    input_stream = InputStream(sys.stdin.read())
    lexer = Example3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Example3Parser(stream)
    parser.full_expr()
    print("Finished")


# warns pb if py file is included in others
if __name__ == '__main__':
    main()
