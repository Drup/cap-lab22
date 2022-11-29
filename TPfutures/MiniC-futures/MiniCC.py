#! /usr/bin/env python3
"""
MiniC-futures Lab. Language Extension for MiniC with future primitives
Usage:
    python3 Main.py <filename>
    python3 Main.py --help
"""
import traceback
from MiniCLexer import MiniCLexer
from MiniCParser import MiniCParser
from MiniCTypingVisitor import MiniCTypingVisitor, MiniCTypeError
from MiniCPPListener import MiniCPPListener
from Errors import MiniCUnsupportedError, MiniCInternalError

import argparse

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

import os
import sys


class CountErrorListener(ErrorListener):
    """Count number of errors.

    Parser provides getNumberOfSyntaxErrors(), but the Lexer
    apparently doesn't provide an easy way to know if an error occured
    after the fact. Do the counting ourserves with a listener.
    """

    def __init__(self):
        super(CountErrorListener, self).__init__()
        self.count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.count += 1

def main(inputname,
         typecheck=True, typecheck_only=False, stdout=False, output_name=None, debug=False):
    (basename, rest) = os.path.splitext(inputname)
    if not typecheck_only:
        if stdout:
            output_name = None
        elif output_name is None:
            output_name = basename + ".cfut"

    input_s = FileStream(inputname, encoding='utf-8')
    lexer = MiniCLexer(input_s)
    counter = CountErrorListener()
    lexer._listeners.append(counter)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    parser._listeners.append(counter)
    tree = parser.prog()
    if counter.count > 0:
        exit(3)  # Syntax or lexicography errors occurred, don't try to go further.

    if typecheck:
        typing_visitor = MiniCTypingVisitor()
        try:
            typing_visitor.visit(tree)
        except MiniCTypeError as e:
            print(e.args[0])
            exit(2)

    if typecheck_only:
        if debug:
            print("Not running code generation because of --disable-codegen.")
        return

    pw = ParseTreeWalker()
    extractor = MiniCPPListener(stream)
    pw.walk(extractor, tree)
    with open(output_name, 'w') if output_name else sys.stdout as output:
        extractor.printrw(output)


# command line management
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate code for .c file')

    parser.add_argument('filename', type=str,
                        help='Source file.')
    parser.add_argument('--stdout', action='store_true',
                        help='Generate code to stdout')
    parser.add_argument('--debug', action='store_true',
                        default=False,
                        help='Emit verbose debug output')
    parser.add_argument('--disable-typecheck', action='store_true',
                        default=False,
                        help="Don't run the typechecker before generating code")
    parser.add_argument('--disable-codegen', action='store_true',
                        default=False,
                        help="Run only the typechecker, don't try generating code.")
    parser.add_argument('--output', type=str,
                        help='Generate code to outfile')

    args = parser.parse_args()

    try:
        main(args.filename,
             not args.disable_typecheck, args.disable_codegen,
             args.stdout, args.output, args.debug,
             )
    except MiniCUnsupportedError as e:
        print(e)
        exit(5)
    except (MiniCInternalError):
        traceback.print_exc()
        exit(4)
