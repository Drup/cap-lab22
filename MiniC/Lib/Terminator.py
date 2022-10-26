"""
MIF08, CAP, CFG library - Terminators.

Each :py:class:`block <Lib.CFG.Block>` of a :py:class:`CFG <Lib.CFG.CFG>`
ends with a branching instruction called a terminator.
There are three kinds of terminators:

- :py:class:`Lib.Statement.AbsoluteJump` is a non-conditional jump
  to another block of the CFG
- :py:class:`BranchingTerminator` is a conditional branching
  instruction with two successor blocks.
  Unlike the class :py:class:`ConditionalJump <Lib.Statement.ConditionalJump>`
  that was used in :py:class:`LinearCode <Lib.LinearCode.LinearCode>`,
  both successor labels have to be specified.
- :py:class:`Return` marks the end of the function

During the construction of the CFG, :py:func:`jump2terminator` builds
a terminator for each extracted chunk of instructions.
"""

from dataclasses import dataclass
from typing import List, Dict
from Lib.Errors import MiniCInternalError
from Lib.Operands import Operand, Renamer, Temporary, Condition
from Lib.Statement import AbsoluteJump, ConditionalJump, Instruction, Label, Statement


@dataclass(unsafe_hash=True)
class Return(Statement):
    """A terminator that marks the end of the function."""

    def __str__(self):
        return ("return")

    def printIns(self, stream):
        print("return", file=stream)

    def targets(self) -> List[Label]:
        """Return the labels targetted by the Return terminator."""
        return []

    def args(self) -> List[Operand]:
        return []

    def rename(self, renamer: Renamer):
        pass

    def substitute(self, subst: Dict[Operand, Operand]):
        if subst != {}:
            raise Exception(
                "substitute: No possible substitution on instruction {}"
                .format(self))
        return self

    def is_read_only(self):
        return True


@dataclass(init=False)
class BranchingTerminator(Instruction):
    """A terminating statement with a condition."""

    #: The condition of the branch
    cond: Condition
    #: The destination label if the condition is true
    label_then: Label
    #: The destination label if the condition is false
    label_else: Label
    #: The first operand of the condition
    op1: Operand
    #: The second operand of the condition
    op2: Operand
    _read_only = True

    def __init__(self, cond: Condition, op1: Operand, op2: Operand,
                 label_then: Label, label_else: Label):
        self.cond = cond
        self.label_then = label_then
        self.label_else = label_else
        self.op1 = op1
        self.op2 = op2
        self.ins = str(self.cond)

    def args(self) -> List[Operand]:
        return [self.op1, self.op2, self.label_then, self.label_else]

    def targets(self) -> List[Label]:
        """Return the labels targetted by the Branching terminator."""
        return [self.label_then, self.label_else]

    def rename(self, renamer: Renamer):
        if isinstance(self.op1, Temporary):
            self.op1 = renamer.replace(self.op1)
        if isinstance(self.op2, Temporary):
            self.op2 = renamer.replace(self.op2)

    def substitute(self, subst: Dict[Operand, Operand]):
        for op in subst:
            if op not in self.args():
                raise Exception(
                    "substitute: Operand {} is not present in instruction {}"
                    .format(op, self))
        op1 = subst.get(self.op1, self.op1) if isinstance(self.op1, Temporary) \
            else self.op1
        op2 = subst.get(self.op2, self.op2) if isinstance(self.op2, Temporary) \
            else self.op2
        return BranchingTerminator(self.cond, op1, op2, self.label_then, self.label_else)

    def __hash__(self):
        return hash(super)


Terminator = Return | AbsoluteJump | BranchingTerminator


def jump2terminator(j: ConditionalJump | AbsoluteJump | None,
                    next_label: Label | None) -> Terminator:
    """
    Construct the Terminator associated to the potential jump j
    to the potential label next_label.
    """
    match j:
        case ConditionalJump():
            if (next_label is None):
                raise MiniCInternalError(
                    "jump2terminator: Missing secondary label for instruction {}"
                    .format(j))
            label_else = next_label
            return BranchingTerminator(j.cond, j.op1, j.op2, j.label, label_else)
        case AbsoluteJump():
            return AbsoluteJump(label=j.label)
        case _:
            if next_label:
                return AbsoluteJump(next_label)
            else:
                return Return()
