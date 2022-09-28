from AritLexer import AritLexer
from AritParser import AritParser
# from AritVisitor import AritVisitor
from MyAritVisitor import MyAritVisitor, UnknownIdentifier

from antlr4 import InputStream, CommonTokenStream
import sys

# example of use of visitors to parse arithmetic expressions.
# stops when the first SyntaxError is launched.


def main():
    lexer = AritLexer(InputStream(sys.stdin.read()))
    stream = CommonTokenStream(lexer)
    parser = AritParser(stream)
    tree = parser.prog()
    print("Parsing : done.")
    visitor = MyAritVisitor()
    try:
        visitor.visit(tree)
    except UnknownIdentifier as exc:
        print('Unknown identifier: {}'.format(exc.args[0]))
        exit(-1)


if __name__ == '__main__':
    main()
