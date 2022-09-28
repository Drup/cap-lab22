#!/usr/bin/env python
from AritLexer import AritLexer
from AritParser import AritParser
import pytest
from MyAritVisitor import MyAritVisitor

from antlr4 import InputStream, CommonTokenStream
import sys


@pytest.mark.parametrize("input, expected", [
    pytest.param('1+1;', 2),
    pytest.param('2-1;', 1),
    pytest.param('2*3;', 6),
    pytest.param('6/2;', 3),
    pytest.param('set x=42; x+1;', 43),
    pytest.param('set x=42; set x=12; x+1;', 13)
])
def test_expr(input, expected):
    lexer = AritLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = AritParser(stream)
    tree = parser.prog()
    print("Parsing : done.")
    visitor = MyAritVisitor()

    def patched_visit(self, ctx):
        self.last_expr = self.visit(ctx.expr())

    visitor.visitExprInstr = patched_visit.__get__(visitor)
    visitor.visit(tree)
    assert visitor.last_expr == expected


if __name__ == '__main__':
    pytest.main(sys.argv)
