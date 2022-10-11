"""
CAP, CodeGeneration, CFG linearization to a list of statements
"""

from typing import List, Set

from Lib.Statement import (
    Statement, AbsoluteJump, ConditionalJump
)
from Lib.Terminator import (Return, BranchingTerminator)
from Lib.CFG import Block


def ordered_blocks_list(cfg) -> List[Block]:
    """
    Compute a list of blocks with optimized ordering for linearization.
    """
    # TODO (Lab4b, Extension)
    return cfg.get_blocks()


def linearize(cfg) -> List[Statement]:
    """
    Linearize the given control flow graph as a list of instructions.
    """
    # TODO (Lab 4b, Exercise 5)
    l: List[Statement] = []  # Linearized CFG
    blocks: List[Block] = ordered_blocks_list(cfg)
    for j, block in enumerate(blocks):
        # 1. Add the label of the block to the linearization
        l.append(block.get_label())
        # 2. Add the body of the block to the linearization
        l.extend(block.get_body())
        # 3. Add the terminator of the block to the linearization
        match block.get_terminator():
            case BranchingTerminator() as j:
                l.append(ConditionalJump(j.cond, j.op1, j.op2, j.label_then))
                l.append(AbsoluteJump(j.label_else))
            case AbsoluteJump() as j:
                l.append(AbsoluteJump(j.label))
            case Return():
                l.append(AbsoluteJump(cfg.get_end()))
    return l
