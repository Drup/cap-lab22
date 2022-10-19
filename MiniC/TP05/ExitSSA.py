"""
CAP, SSA Intro, Elimination and Optimisations
Functions to convert a CFG out of SSA Form.
"""

from typing import cast, List, Set, Tuple
from Lib import RiscV
from Lib.Graphes import DiGraph
from Lib.CFG import Block, BlockInstr, CFG
from Lib.Operands import (
    Register, DataLocation,
    Temporary)
from Lib.Statement import AbsoluteJump
from Lib.Terminator import BranchingTerminator, Return
from Lib.PhiNode import PhiNode


def generate_moves_from_phis(phis: List[PhiNode], parent: Block) -> List[BlockInstr]:
    """
    `generate_moves_from_phis(phis, parent)` builds a list of move instructions
    to be inserted in a new block between `parent` and the block with phi nodes
    `phis`.

    This is an helper function called during SSA exit.
    """
    moves: List[BlockInstr] = []
    # TODO compute 'moves', a list of 'mv' instructions to insert under parent
    # (Lab 5a, Exercise 6)
    return moves


def exit_ssa(cfg: CFG, is_smart: bool) -> None:
    """
    `exit_ssa(cfg)` replaces phi nodes with move instructions to exit SSA form.

    `is_smart` is set to true when smart register allocation is enabled (Lab 5b).
    """
    for b in cfg.get_blocks():
        phis = cast(List[PhiNode], b._phis)  # Use cast for Pyright
        b._phis = []  # Remove all phi nodes in the block
        parents: List[Block] = b.get_in().copy()  # Copy as we modify it by adding blocks
        for parent in parents:
            moves = generate_moves_from_phis(phis, parent)
            # TODO Add the block containing 'moves' to 'cfg'
            # and update edges and jumps accordingly (Lab 5a, Exercise 6)
            raise NotImplementedError("exit_ssa")


