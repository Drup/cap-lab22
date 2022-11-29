"""
This file defines the base class :py:class:`FunctionData`,
containing metadata on a RiscV function, as well as utility
functions common to the different intermediate representations.
"""

from typing import (List, Callable, TypeVar)
from Lib.Errors import AllocationError
from Lib.Operands import (
    Offset, Temporary, TemporaryPool,
    S, T, FP)
from Lib.Statement import (Statement, Instruction, Label, Comment)


class FunctionData:
    """
    Stores some metadata on a RiscV function:
    name of the function, label names, temporary variables
    (using :py:class:`Lib.Operands.TemporaryPool`),
    and div_by_zero label.

    This class is usually used indirectly through the
    different intermediate representations we work with,
    such as :py:attr:`Lib.LinearCode.LinearCode.fdata`.
    """

    _nblabel: int
    _dec: int
    _pool: TemporaryPool
    _name: str
    _label_div_by_zero: Label

    def __init__(self, name: str):
        self._nblabel = -1
        self._dec = 0
        self._pool = TemporaryPool()
        self._name = name
        self._label_div_by_zero = self.fresh_label("div_by_zero")

    def get_name(self) -> str:
        """Return the name of the function."""
        return self._name

    def fresh_tmp(self) -> Temporary:
        """
        Return a new fresh Temporary,
        which is added to the pool.
        """
        return self._pool.fresh_tmp()

    def fresh_offset(self) -> Offset:
        """
        Return a new offset in the memory stack.
        Offsets are decreasing relative to FP.
        """
        self._dec = self._dec + 1
        # For ld or sd, an offset on 12 signed bits is expected
        # Raise an error if the offset is too big
        if -8 * self._dec < - 2 ** 11:
            raise AllocationError(
                    "Offset given by the allocation too big to be manipulated ({}), sorry."
                    .format(self._dec))
        return Offset(FP, -8 * self._dec)

    def get_offset(self) -> int:
        """
        Return the current offset in the memory stack.
        """
        return self._dec

    def _fresh_label_name(self, name) -> str:
        """
        Return a new unique label name based on the given string.
        """
        self._nblabel = self._nblabel + 1
        return name + "_" + str(self._nblabel) + "_" + self._name

    def fresh_label(self, name) -> Label:
        """
        Return a new label, with a unique name based on the given string.
        """
        return Label(self._fresh_label_name(name))

    def get_label_div_by_zero(self) -> Label:
        return self._label_div_by_zero


_T = TypeVar("_T", bound=Statement)


def _iter_statements(
        listIns: List[_T], f: Callable[[_T], List[_T]]) -> List[_T | Comment]:
    """Iterate over instructions.
    For each real instruction i (not label or comment), replace it
    with the list of instructions given by f(i).
    """
    newListIns: List[_T | Comment] = []
    for old_i in listIns:
        # Do nothing for label or comment
        if not isinstance(old_i, Instruction):
            newListIns.append(old_i)
            continue
        new_i_list = f(old_i)
        # Otherwise, replace the instruction by the list
        # returned by f, with comments giving the replacement
        newListIns.append(Comment("Replaced " + str(old_i)))
        newListIns.extend(new_i_list)
    return newListIns


def _print_code(listIns: List, fdata: FunctionData, output,
                init_label=None, fin_label=None, fin_div0=False, comment=None) -> None:
    """
    Please use print_code from LinearCode or CFG, not directly this one.

    Print the instructions from listIns, forming fdata, on output.
    If init_label is given, add an initial jump to it before the generated code.
    If fin_label is given, add it after the generated code.
    If fin_div0 is given equal to true, add the code for returning an
    error when dividing by 0, at the very end.
    """
    # compute size for the local stack - do not forget to align by 16
    fo = fdata.get_offset()  # allocate enough memory for stack
    # Room for S_i (except S_0 which is fp) and T_i backup
    fo += len(S[1:]) + len(T)
    cardoffset = 8 * (fo + (0 if fo % 2 == 0 else 1)) + 16
    output.write(
        "##Automatically generated RISCV code, MIF08 & CAP\n")
    if comment is not None:
        output.write("##{} version\n".format(comment))
    output.write("\n\n##prelude\n")
    # We put an li t0, cardoffset in case it is greater than 2**11
    # We use t0 because it is caller-saved
    output.write("""
        .text
        .globl {0}
{0}:
        li t0, {1}
        sub sp, sp, t0
        sd ra, 0(sp)
        sd fp, 8(sp)
        add fp, sp, t0
""".format(fdata.get_name(), cardoffset))
    # Stack in RiscV is managed with SP
    if init_label is not None:
        # Add a jump to init_label before the generated code.
        output.write("""
        j {0}
""".format(init_label))
    output.write("\n\n##Generated Code\n")
    # Generated code
    for i in listIns:
        i.printIns(output)
    output.write("\n\n##postlude\n")
    if fin_label is not None:
        # Add fin_label after the generated code.
        output.write("""
{0}:
""".format(fin_label))
    # We put an li t0, cardoffset in case it is greater than 2**11
    # We use t0 because it is caller-saved
    output.write("""
        ld ra, 0(sp)
        ld fp, 8(sp)
        li t0, {0}
        add sp, sp, t0
        ret
""".format(cardoffset))
    if fin_div0:
        # Add code for division by 0 at the end.
        output.write("""
{0}:
        la a0, {0}_msg
        call println_string
        li a0, 1
        call exit
""".format(fdata._label_div_by_zero))
    # Add the data for the message of the division by 0
    output.write("""
{0}_msg:  .string "Division by 0"
""".format(fdata._label_div_by_zero))
