"""
CAP, CodeGeneration, LinearCode API
Classes for a RiscV linear code.
"""

from typing import List
from Lib.Operands import (A0, Function, DataLocation)
from Lib.Statement import (
    Instru3A, AbsoluteJump, ConditionalJump, Comment, Label
)
from Lib.RiscV import (mv, call)
from Lib.FunctionData import (FunctionData, _iter_statements, _print_code)


CodeStatement = Comment | Label | Instru3A | AbsoluteJump | ConditionalJump


class LinearCode:
    """
    Representation of a RiscV program as a list of instructions.

    :py:meth:`add_instruction` is repeatedly called in the codegen visitor
    to build a complete list of RiscV instructions for the source program.

    The :py:attr:`fdata` member variable contains some meta-information
    on the program, for instance to allocate a new temporary.
    See :py:class:`Lib.FunctionData.FunctionData`.

    For debugging purposes, :py:meth:`print_code` allows to print
    the RiscV program to a file.
    """

    """
    The :py:attr:`fdata` member variable contains some meta-information
    on the program, for instance to allocate a new temporary.
    See :py:class:`Lib.FunctionData.FunctionData`.
    """
    fdata: FunctionData

    _listIns: List[CodeStatement]

    def __init__(self, name: str):
        self._listIns = []
        self.fdata = FunctionData(name)

    def add_instruction(self, i: CodeStatement) -> None:
        """
        Utility function to add an instruction in the program.

        See also :py:mod:`Lib.RiscV` to generate relevant instructions.
        """
        self._listIns.append(i)

    def iter_statements(self, f) -> None:
        """Iterate over instructions.
        For each real instruction (not label or comment), call f,
        which must return either None or a list of instruction. If it
        returns None, nothing happens. If it returns a list, then the
        instruction is replaced by this list.
        """
        self._listIns = _iter_statements(self._listIns, f)

    def get_instructions(self) -> List[CodeStatement]:
        """Return the list of instructions of the program."""
        return self._listIns

    # each instruction has its own "add in list" version
    def add_label(self, s: Label) -> None:
        """Add a label in the program."""
        return self.add_instruction(s)

    def add_comment(self, s: str) -> None:
        """Add a comment in the program."""
        self.add_instruction(Comment(s))

    def add_instruction_PRINTLN_INT(self, reg: DataLocation) -> None:
        """Print integer value, with newline. (see Expand)"""
        # a print instruction generates the temp it prints.
        self.add_instruction(mv(A0, reg))
        self.add_instruction(call(Function('println_int')))

    def __str__(self):
        return '\n'.join(map(str, self._listIns))

    def print_code(self, output, comment=None) -> None:
        """Outputs the RiscV program as text to a file at the given path."""
        _print_code(self._listIns, self.fdata, output, init_label=None,
                    fin_label=None, fin_div0=True, comment=comment)

    def print_dot(self, filename: str, DF=None, view=False) -> None:  # pragma: no cover
        """Outputs the RiscV program as graph to a file at the given path."""
        # import graphviz here so that students who don't have it can still work on lab4
        from graphviz import Digraph
        graph = Digraph()
        # nodes
        content = ""
        for i in self._listIns:
            content += str(i) + "\\l"
        graph.node("Code", label=content, shape='rectangle')
        # no edges
        graph.render(filename, view=view)
