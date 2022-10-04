"""
This file defines the base class :py:class:`Allocator`
and the naïve implementation :py:class:`NaiveAllocator`.
"""

from Lib.Operands import Temporary, Operand, DataLocation, GP_REGS
from Lib.Statement import Instruction
from Lib.Errors import AllocationError
from Lib.FunctionData import FunctionData
from typing import Dict, List


class Allocator():
    """General base class for Naive, AllInMem and Smart Allocators.
    Replace all temporaries in the code with actual data locations.

    Allocation is done in two steps:

    - First, :py:meth:`prepare` is responsible for calling
      :py:meth:`Lib.Operands.TemporaryPool.set_temp_allocation`
      with a mapping from temporaries to where they should actually be stored
      (in registers or in memory).
    - Then, :py:meth:`replace` is called for each instruction in order to
      replace the temporary operands with the previously assigned locations
      (and possibly add some instructions before or after).
      Concretely, it returns a list of instructions that should replace the original
      instruction. The actual iteration over all the instructions is handled transparently
      by :py:meth:`Lib.LinearCode.LinearCode.iter_statements`.
    """

    _fdata: FunctionData

    def __init__(self, fdata: FunctionData):
        self._fdata = fdata

    def prepare(self) -> None:  # pragma: no cover
        pass

    def replace(self, instr: Instruction) -> List[Instruction]:
        """Transform an instruction with temporaries into a list of instructions."""
        return [instr]

    def rewriteCode(self, listcode) -> None:
        """Modify the code to replace temporaries with
        registers or memory locations.
        """
        listcode.iter_statements(self.replace)


class NaiveAllocator(Allocator):
    """Naive Allocator: try to assign a register to each temporary,
    fails if there are more temporaries than registers.
    """

    def replace(self, old_instr: Instruction) -> List[Instruction]:
        """Replace Temporary operands with the corresponding allocated Register."""
        subst: Dict[Operand, Operand] = {}
        for arg in old_instr.args():
            if isinstance(arg, Temporary):
                subst[arg] = arg.get_alloced_loc()
        new_instr = old_instr.substitute(subst)
        return [new_instr]

    def prepare(self) -> None:
        """Allocate all temporaries to registers.
        Fail if there are too many temporaries."""
        regs = list(GP_REGS)  # Get a writable copy
        temp_allocation: Dict[Temporary, DataLocation] = dict()
        for tmp in self._fdata._pool.get_all_temps():
            try:
                reg = regs.pop()
            except IndexError:
                raise AllocationError(
                    "Too many temporaries ({}) for the naive allocation, sorry."
                    .format(len(self._fdata._pool.get_all_temps())))
            temp_allocation[tmp] = reg
        self._fdata._pool.set_temp_allocation(temp_allocation)
