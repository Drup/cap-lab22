"""
CAP, SSA Intro, Elimination and Optimisations
Functions to convert a CFG into SSA Form.
"""

from typing import List, Dict, Set
from Lib.CFG import Block, CFG
from Lib.Operands import Renamer
from Lib.Statement import Instruction
from Lib.PhiNode import PhiNode
from Lib.Dominators import computeDom, computeDT, computeDF


def insertPhis(cfg: CFG, DF: Dict[Block, Set[Block]]) -> None:
    """
    `insertPhis(CFG, DF)` inserts phi nodes in `cfg` where needed.
    At this point, phi nodes will look like `temp_x = φ(temp_x, ..., temp_x)`.

    This is an helper function called during SSA entry.
    """
    for var, defs in cfg.gather_defs().items():
        has_phi: Set[Block] = set()
        queue: List[Block] = list(defs)
        while queue:
            d = queue.pop(0)
            for b in DF[d]:
                if b not in has_phi:
                    # TODO add a phi node in block `b` (Lab 5a, Exercise 4)
                    raise NotImplementedError("insertPhis")


def rename_block(cfg: CFG, DT: Dict[Block, Set[Block]], renamer: Renamer, b: Block) -> None:
    """
    Rename variables from block b.

    This is an auxiliary function for `rename_variables`.
    """
    renamer = renamer.copy()
    for i in b.get_all_statements():
        if isinstance(i, Instruction | PhiNode):
            i.rename(renamer)
    for succ in cfg.out_blocks(b):
        for i in succ._phis:
            assert (isinstance(i, PhiNode))
            i.rename_from(renamer, b.get_label())
    # TODO recursive call(s) of rename_block (Lab 5a, Exercise 5)


def rename_variables(cfg: CFG, DT: Dict[Block, Set[Block]]) -> None:
    """
    Rename variables in the CFG, to transform `temp_x = φ(temp_x, ..., temp_x)`
    into `temp_x = φ(temp_0, ... temp_n)`.

    This is an helper function called during SSA entry.
    """
    renamer = Renamer(cfg.fdata._pool)
    # TODO initial call(s) to rename_block (Lab 5a, Exercise 5)


def enter_ssa(cfg: CFG, dom_graphs=False, basename="prog") -> None:
    """
    Convert the CFG `cfg` into SSA Form:
    compute the dominance frontier, then insert phi nodes and finally
    rename variables accordingly.

    `dom_graphs` indicates if we have to print the domination graphs.
    `basename` is used for the names of the produced graphs.
    """
    # TODO implement this function (Lab 5a, Exercise 2)
    raise NotImplementedError("enter_ssa")
