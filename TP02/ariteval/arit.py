#! /usr/bin/env python3
"""
Usage:
    python3 arit.py <filename>
"""
# Main file for MIF08 - Lab03 - 2018, changed in 2022

from AritLexer import AritLexer
from AritParser import AritParser, UnknownIdentifier, DivByZero
from antlr4 import FileStream, CommonTokenStream, StdinStream
from antlr4.tree.Trees import Trees
from antlr4.Utils import escapeWhitespace

import argparse


def getNodeText(node, parser):
    return escapeWhitespace(Trees.getNodeText(node, recog=parser), True).replace('\\', '\\\\')


def _toDot(t, g, parser):
    for c in Trees.getChildren(t):
        g.node(str(id(c)), getNodeText(c, parser))
        g.edge(str(id(t)), str(id(c)))
        _toDot(c, g, parser)


def toDot(t, parser):
    from graphviz import Digraph
    g = Digraph()
    g.node(str(id(t)), getNodeText(t, parser))
    _toDot(t, g, parser)
    g.render("tree.dot", view=True)


def main(inputname, lisp, debug):
    if inputname is None:
        lexer = AritLexer(StdinStream())
    else:
        lexer = AritLexer(FileStream(inputname))
    stream = CommonTokenStream(lexer)
    parser = AritParser(stream)
    try:
        tree = parser.prog()
        if lisp:
            print(tree.toStringTree(tree, parser))
        if debug:
            toDot(tree, parser)
    except UnknownIdentifier as exc:  # Parser's exception
        print('{} is undefined'.format(exc.args[0]))
        exit(1)
    except DivByZero:
        print('Division by zero')
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AritEval lab')
    parser.add_argument('filename', type=str, nargs='?', help='Source file.')
    parser.add_argument('--lisp', default=False, action='store_true',
                        help="Print parse tree in Lisp format")
    parser.add_argument('--debug', default=False, action='store_true',
                        help="Print parse tree graphically")
    args = parser.parse_args()
    main(args.filename, args.lisp, args.debug)
