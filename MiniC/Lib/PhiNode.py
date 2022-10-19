"""
Classes for φ nodes in a RiscV CFG :py:class:`CFG <Lib.CFG.CFG>` under SSA Form:
:py:class:`PhiNode` for a statement of the form temp_x = φ(temp_0, ..., temp_n).
These particular kinds of statements are expected to be in the field
b._phis for a :py:class:`Block <Lib.CFG.Block>` b.
"""

from dataclasses import dataclass
from typing import Dict

from Lib.Operands import Operand, Temporary, DataLocation, Renamer
from Lib.Statement import Statement, Label


@dataclass
class PhiNode(Statement):
    """
    A φ node is a renaming in the CFG, of the form temp_x = φ(temp_0, ..., temp_n).
    The field var contains the variable temp_x.
    The field srcs relies for each precedent block in the CFG, identified with its label,
    the variable temp_i of the φ node.
    """
    var: DataLocation
    srcs: Dict[Label, Operand]

    def defined(self):
        """Return the variable defined by the φ node."""
        return [self.var]

    def used(self) -> Dict[Label, Operand]:
        """
        Return the dictionnary associating for each previous block the corresponding variable.
        """
        return self.srcs

    def rename(self, renamer: Renamer) -> None:
        """Rename the variable defined by the φ node with a fresh name."""
        if isinstance(self.var, Temporary):
            self.var = renamer.fresh(self.var)

    def rename_from(self, renamer: Renamer, label: Label) -> None:
        """Rename the variable associated to the block identified by `label`."""
        if label in self.srcs:
            t = self.srcs[label]
            if isinstance(t, Temporary):
                if renamer.defined(t):
                    self.srcs[label] = renamer.replace(t)
                else:
                    del self.srcs[label]

    def __str__(self):
        return "{} = φ({})".format(self.var, self.srcs)

    def __hash__(self):
        return hash((self.var, *self.srcs.items()))

    def printIns(self, stream):
        print('        # ' + str(self), file=stream)
