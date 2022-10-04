"""
This file defines the base class :py:class:`Operand`
and its subclasses for different operands: :py:class:`Condition`,
:py:class:`DataLocation` and :py:class:`Function`.

The class :py:class:`DataLocation` itself has subclasses:
:py:class:`Register`, :py:class:`Offset` for address in memory,
:py:class:`Immediate` for constants and :py:class:`Temporary`
for location not yet allocated.

This file also define shortcuts for registers in RISCV.
"""

from typing import Dict, List
from MiniCParser import MiniCParser
from Lib.Errors import MiniCInternalError


class Operand():

    pass


# signed version for riscv
all_ops = ['blt', 'bgt', 'beq', 'bne', 'ble', 'bge', 'beqz', 'bnez']
opdict = {MiniCParser.LT:   'blt', MiniCParser.GT:   'bgt',
          MiniCParser.LTEQ: 'ble', MiniCParser.GTEQ: 'bge',
          MiniCParser.NEQ:  'bne', MiniCParser.EQ:   'beq'}
opnot_dict = {'bgt': 'ble',
              'bge': 'blt',
              'blt': 'bge',
              'ble': 'bgt',
              'beq': 'bne',
              'bne': 'beq',
              'beqz': 'bnez',
              'bnez': 'beqz'}


class Condition(Operand):
    """Condition, i.e. comparison operand for a CondJump.

    Example usage :

    - Condition('beq') = branch if equal.
    - Condition(MiniCParser.LT) = branch if lower than.
    - ...

    The constructor's argument shall be a string in the list all_ops, or a
    comparison operator in MiniCParser.LT, MiniCParser.GT, ... (one of the keys
    in opdict).

    A 'negate' method allows getting the negation of this condition.
    """

    _op: str

    def __init__(self, optype):
        if optype in opdict:
            self._op = opdict[optype]
        elif str(optype) in all_ops:
            self._op = str(optype)
        else:
            raise MiniCInternalError("Unsupported comparison operator %s", optype)

    def negate(self) -> 'Condition':
        """Return the opposite condition."""
        return Condition(opnot_dict[self._op])

    def __str__(self):
        return self._op


class Function(Operand):
    """Operand for build-in function call."""

    _name: str

    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return self._name


class DataLocation(Operand):
    """ A Data Location is either a register, a temporary
    or a place in memory (offset).
    """

    pass


# map for register shortcuts
reg_map = dict([(0, 'zero'), (1, 'ra'), (2, 'sp')] +  # no (3, 'gp') nor (4, 'tp')
               [(i+5, 't'+str(i)) for i in range(3)] +
               [(8, 'fp'), (9, 's1')] +
               [(i+10, 'a'+str(i)) for i in range(8)] +
               [(i+18, 's'+str(i+2)) for i in range(10)] +
               [(i+28, 't'+str(i+3)) for i in range(4)])


class Register(DataLocation):
    """ A (physical) register."""

    _number: int

    def __init__(self, number: int):
        self._number = number

    def __repr__(self):
        if self._number not in reg_map:
            raise Exception("Register number %d should not be used", self._number)
        else:
            return ("{}".format(reg_map[self._number]))

    def __eq__(self, other):
        return isinstance(other, Register) and self._number == other._number

    def __hash__(self):
        return self._number


# Shortcuts for registers in RISCV
# Only integer registers
ZERO = Register(0)
RA = Register(1)
SP = Register(2)
GP = Register(3)  # Register not used for this course
TP = Register(4)  # Register not used for this course
A = tuple(Register(i + 10) for i in range(8))
S = tuple(Register(i + 8) for i in range(2)) + tuple(Register(i + 18) for i in range(10))
T = tuple(Register(i + 5) for i in range(3)) + tuple(Register(i + 28) for i in range(4))
A0 = A[0]  # function args/return Values: A0, A1
A1 = A[1]
FP = S[0]  # Frame Pointer = Saved register 0

# General purpose registers, usable for the allocator
GP_REGS = S[4:] + T  # s0, s1, s2 and s3 are special


class Offset(DataLocation):
    """ Offset = address in memory computed with base + offset."""

    _basereg: Register
    _offset: int

    def __init__(self, basereg: Register, offset: int):
        self._basereg = basereg
        self._offset = offset

    def __repr__(self):
        return ("{}({})".format(self._offset, self._basereg))

    def get_offset(self) -> int:
        """Return the value of the offset."""
        return self._offset


class Immediate(DataLocation):
    """Immediate operand (integer)."""

    _val: int

    def __init__(self, val):
        self._val = val

    def __str__(self):
        return str(self._val)


class Temporary(DataLocation):
    """Temporary, a location that has not been allocated yet.
    It will later be mapped to a physical register (Register) or to a memory location (Offset).
    """

    _number: int
    _pool: 'TemporaryPool'

    def __init__(self, number: int, pool: 'TemporaryPool'):
        self._number = number
        self._pool = pool

    def __repr__(self):
        return ("temp_{}".format(str(self._number)))

    def get_alloced_loc(self) -> DataLocation:
        """Return the DataLocation allocated to this Temporary."""
        return self._pool.get_alloced_loc(self)


class TemporaryPool:
    """Manage a pool of temporaries."""

    _all_temps: List[Temporary]
    _current_num: int
    _allocation: Dict[Temporary, DataLocation]

    def __init__(self):
        self._all_temps = []
        self._current_num = 0
        self._allocation = dict()

    def get_all_temps(self) -> List[Temporary]:
        """Return all the temporaries of the pool."""
        return self._all_temps

    def get_alloced_loc(self, t: Temporary) -> DataLocation:
        """Get the actual DataLocation allocated for the temporary t."""
        return self._allocation[t]

    def add_tmp(self, t: Temporary):
        """Add a temporary to the pool."""
        self._all_temps.append(t)
        self._allocation[t] = t  # While no allocation, return the temporary itself

    def set_temp_allocation(self, allocation: Dict[Temporary, DataLocation]) -> None:
        """Give a mapping from temporaries to actual registers.
        The argument allocation must be a dict from Temporary to
        DataLocation other than Temporary (typically Register or Offset).
        Typing enforces that keys are Temporary and values are Datalocation.
        We check the values are indeed not Temporary.
        """
        for v in allocation.values():
            assert not isinstance(v, Temporary), (
                "Incorrect allocation scheme: value " +
                str(v) + " is a Temporary.")
        self._allocation = allocation

    def fresh_tmp(self) -> Temporary:
        """Give a new fresh Temporary and add it to the pool."""
        t = Temporary(self._current_num, self)
        self._current_num += 1
        self.add_tmp(t)
        return t


class Renamer:
    """Manage a renaming of temporaries."""

    _pool: TemporaryPool
    _env: Dict[Temporary, Temporary]

    def __init__(self, pool: TemporaryPool):
        self._pool = pool
        self._env = dict()

    def fresh(self, t: Temporary) -> Temporary:
        """Give a fresh rename for a Temporary."""
        new_t = self._pool.fresh_tmp()
        self._env[t] = new_t
        return new_t

    def replace(self, t: Temporary) -> Temporary:
        """Give the rename for a Temporary (which is itself if it is not renamed)."""
        return self._env.get(t, t)

    def defined(self, t: Temporary) -> bool:
        """True if the Temporary is renamed."""
        return t in self._env

    def copy(self):
        """Give a copy of the Renamer."""
        r = Renamer(self._pool)
        r._env = self._env.copy()
        return r
