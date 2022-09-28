# Visitor to *typecheck* MiniC files
from typing import List
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.Errors import MiniCInternalError, MiniCTypeError

from enum import Enum


class BaseType(Enum):
    Float, Integer, Boolean, String = range(4)


# Basic Type Checking for MiniC programs.
class MiniCTypingVisitor(MiniCVisitor):

    def __init__(self):
        self._memorytypes = dict()  # id -> types
        # For now, we don't have real functions ...
        self._current_function = "main"

    def _raise(self, ctx, for_what, *types):
        raise MiniCTypeError(
            'In function {}: Line {} col {}: invalid type for {}: {}'.format(
                self._current_function,
                ctx.start.line, ctx.start.column, for_what,
                ' and '.join(t.name.lower() for t in types)))

    def _assertSameType(self, ctx, for_what, *types):
        if not all(types[0] == t for t in types):
            raise MiniCTypeError(
                'In function {}: Line {} col {}: type mismatch for {}: {}'.format(
                    self._current_function,
                    ctx.start.line, ctx.start.column, for_what,
                    ' and '.join(t.name.lower() for t in types)))

    def _raiseNonType(self, ctx, message):
        raise MiniCTypeError(
            'In function {}: Line {} col {}: {}'.format(
                self._current_function,
                ctx.start.line, ctx.start.column, message))

    # type declaration

    def visitVarDecl(self, ctx) -> None:
        raise NotImplementedError()

    def visitBasicType(self, ctx):
        assert ctx.mytype is not None
        if ctx.mytype.type == MiniCParser.INTTYPE:
            return BaseType.Integer
        elif ctx.mytype.type == MiniCParser.FLOATTYPE:
            return BaseType.Float
        else:  # TODO: same for other types
            raise NotImplementedError()

    def visitIdList(self, ctx) -> List[str]:
        raise NotImplementedError()

    def visitIdListBase(self, ctx) -> List[str]:
        raise NotImplementedError()

    # typing visitors for expressions, statements !

    # visitors for atoms --> type
    def visitParExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx):
        return BaseType.Integer

    def visitFloatAtom(self, ctx):
        return BaseType.Float

    def visitBooleanAtom(self, ctx):
        raise NotImplementedError()

    def visitIdAtom(self, ctx):
        try:
            return self._memorytypes[ctx.getText()]
        except KeyError:
            self._raiseNonType(ctx,
                               "Undefined variable {}".format(ctx.getText()))

    def visitStringAtom(self, ctx):
        return BaseType.String

    # now visit expr

    def visitAtomExpr(self, ctx):
        return self.visit(ctx.atom())

    def visitOrExpr(self, ctx):
        raise NotImplementedError()

    def visitAndExpr(self, ctx):
        raise NotImplementedError()

    def visitEqualityExpr(self, ctx):
        raise NotImplementedError()

    def visitRelationalExpr(self, ctx):
        raise NotImplementedError()

    def visitAdditiveExpr(self, ctx):
        assert ctx.myop is not None
        raise NotImplementedError()

    def visitMultiplicativeExpr(self, ctx):
        raise NotImplementedError()

    def visitNotExpr(self, ctx):
        raise NotImplementedError()

    def visitUnaryMinusExpr(self, ctx):
        raise NotImplementedError()

    # visit statements

    def visitPrintlnintStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Integer:
            self._raise(ctx, 'println_int statement', etype)

    def visitPrintlnfloatStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Float:
            self._raise(ctx, 'println_float statement', etype)

    def visitPrintlnboolStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Boolean:
            self._raise(ctx, 'println_int statement', etype)

    def visitPrintlnstringStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.String:
            self._raise(ctx, 'println_string statement', etype)

    def visitAssignStat(self, ctx):
        raise NotImplementedError()

    def visitWhileStat(self, ctx):
        raise NotImplementedError()

    def visitIfStat(self, ctx):
        raise NotImplementedError()
