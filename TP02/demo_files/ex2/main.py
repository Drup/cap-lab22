from antlr4 import InputStream
from antlr4 import CommonTokenStream

# include to use the generated lexer and parser
from Example2Lexer import Example2Lexer
from Example2Parser import Example2Parser

import sys


def main():
    input_stream = InputStream(sys.stdin.read())
    lexer = Example2Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Example2Parser(stream)
    parser.full_expr()  # We want to recognize full_expr in the grammar Example2
    print("Finished")


# warns pb if py file is included in others
if __name__ == '__main__':
    main()
