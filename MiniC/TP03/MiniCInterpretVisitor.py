# Visitor to *interpret* MiniC files
from typing import Dict, List, cast
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.Errors import MiniCRuntimeError, MiniCInternalError

MINIC_VALUE = int | str | bool | float | List['MINIC_VALUE']


class MiniCInterpretVisitor(MiniCVisitor):

    _memory: Dict[str, MINIC_VALUE]

    def __init__(self):
        self._memory = dict()  # store all variable ids and values.
        self.has_main = False

    # visitors for variable declarations

    def visitVarDecl(self, ctx) -> None:
        # Initialise all variables in self._memory
        type_str = ctx.typee().getText()
        raise NotImplementedError()

    def visitIdList(self, ctx) -> List[str]:
        raise NotImplementedError()

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # visitors for atoms --> value

    def visitParExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> int:
        return int(ctx.getText())

    def visitFloatAtom(self, ctx) -> float:
        return float(ctx.getText())

    def visitBooleanAtom(self, ctx) -> bool:
        return ctx.getText() == "true"

    def visitIdAtom(self, ctx) -> MINIC_VALUE:
        raise NotImplementedError()

    def visitStringAtom(self, ctx) -> str:
        return ctx.getText()[1:-1]  # Remove the ""

    # visit expressions

    def visitAtomExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.atom())

    def visitOrExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        return lval | rval

    def visitAndExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        return lval & rval

    def visitEqualityExpr(self, ctx) -> bool:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        # be careful for float equality
        if ctx.myop.type == MiniCParser.EQ:
            return lval == rval
        else:
            return lval != rval

    def visitRelationalExpr(self, ctx) -> bool:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.LT:
            return lval < rval
        elif ctx.myop.type == MiniCParser.LTEQ:
            return lval <= rval
        elif ctx.myop.type == MiniCParser.GT:
            return lval > rval
        elif ctx.myop.type == MiniCParser.GTEQ:
            return lval >= rval
        else:
            raise MiniCInternalError(
                "Unknown comparison operator '%s'" % ctx.myop
            )

    def visitAdditiveExpr(self, ctx) -> MINIC_VALUE:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.PLUS:
            if any(isinstance(x, str) for x in (lval, rval)):
                return '{}{}'.format(lval, rval)
            else:
                return lval + rval
        elif ctx.myop.type == MiniCParser.MINUS:
            return lval - rval
        else:
            raise MiniCInternalError(
                "Unknown additive operator '%s'" % ctx.myop)

    def visitMultiplicativeExpr(self, ctx) -> MINIC_VALUE:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.MULT:
            return lval * rval
        elif ctx.myop.type == MiniCParser.DIV:
            if rval == 0:
                raise MiniCRuntimeError("Division by 0")
            if isinstance(lval, int):
                return lval // rval
            else:
                return lval / rval
        elif ctx.myop.type == MiniCParser.MOD:
            # TODO : interpret modulo
            raise NotImplementedError()
        else:
            raise MiniCInternalError(
                "Unknown multiplicative operator '%s'" % ctx.myop)

    def visitNotExpr(self, ctx) -> bool:
        return not self.visit(ctx.expr())

    def visitUnaryMinusExpr(self, ctx) -> MINIC_VALUE:
        return -self.visit(ctx.expr())

    # visit statements

    def visitPrintlnintStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        print(val)

    def visitPrintlnfloatStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        if isinstance(val, float):
            val = "%.2f" % val
        print(val)

    def visitPrintlnboolStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        print('1' if val else '0')

    def visitPrintlnstringStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        print(val)

    def visitAssignStat(self, ctx) -> None:
        raise NotImplementedError()

    def visitIfStat(self, ctx) -> None:
        raise NotImplementedError()

    def visitWhileStat(self, ctx) -> None:
        raise NotImplementedError()

    # TOPLEVEL
    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)
        if not self.has_main:
            # A program without a main function is compilable (hence
            # it's not a typing error per se), but not executable,
            # hence we consider it a runtime error.
            raise MiniCRuntimeError("No main function in file")

    # Visit a function: ignore if non main!
    def visitFuncDef(self, ctx) -> None:
        funname = ctx.ID().getText()
        if funname == "main":
            self.has_main = True
            self.visit(ctx.vardecl_l())
            self.visit(ctx.block())
