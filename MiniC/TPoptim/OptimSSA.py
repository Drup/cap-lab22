"""
CAP, SSA Intro, Elimination and Optimisations
Optimisations on SSA.
"""

from enum import Enum
from typing import List, Dict, Tuple, cast
from Lib.Errors import MiniCInternalError
from Lib.Operands import (Operand, Temporary, Immediate, A, ZERO)
from Lib.Statement import (Statement, Instruction, Label, AbsoluteJump)
from Lib.CFG import (BlockInstr, Terminator, Block, CFG)
from Lib.Terminator import (Return, BranchingTerminator)
from Lib.PhiNode import PhiNode
from Lib import RiscV


def div_rd_0(a: int, b: int) -> int:
    """Division rounded towards 0 (integer division in Python rounds down)."""
    return -(-a // b) if (a < 0) ^ (b < 0) else a // b


def mod_rd_0(a: int, b: int) -> int:
    """Modulo rounded towards 0 (integer division in Python rounds down)."""
    return -(-a % b) if (a < 0) ^ (b < 0) else a % b


class Lattice(Enum):
    Bottom = 0
    Top = 1


LATTICE_VALUE = int | Lattice  # Type for our values: Bottom < int < Top


def join(v1: LATTICE_VALUE, v2: LATTICE_VALUE) -> LATTICE_VALUE:
    """Compute the join of the two lattice values."""
    match v1, v2:
        case Lattice.Top, _:
            return Lattice.Top
        case _, Lattice.Top:
            return Lattice.Top
        case Lattice.Bottom, _:
            return v2
        case _, Lattice.Bottom:
            return v1
        case _, _:  # both int
            if v1 == v2:
                return v1
            else:
                return Lattice.Top


def joinl(values: List[LATTICE_VALUE]) -> LATTICE_VALUE:
    """Compute the join of the list of lattice values."""
    res = Lattice.Bottom
    for v in values:
        res = join(res, v)
    return res


def has_top(values: List[LATTICE_VALUE]) -> bool:
    """True if Top is in values."""
    return any(x == Lattice.Top for x in values)


def has_bottom(values: List[LATTICE_VALUE]) -> bool:
    """True if Bottom is in values."""
    return any(x == Lattice.Bottom for x in values)


class CondConstantPropagation:
    """
    Class that optimises a CFG under SSA form
    following the algorithm "Sparse Conditionnal Constant Propagation".
    """

    cfg: CFG
    # CFG under SSA form to optimise

    valueness: Dict[Operand, LATTICE_VALUE]
    # Values of each variable v:
    # valueness[v] = Lattice.Bottom if no evidence that v is assigned
    # valueness[v] = n if we found evidence that only n is assigned to v
    # valueness[v] = Lattice.Top if we found evidence that v is assigned
    # to at least two different values

    executability: Dict[Tuple[Block | None, Block], bool]
    # Exectuability of an edge (B, C):
    # executability[B, C] = False if no evidence that the edge (B, C) can ever be executed
    # executability[B, C] = True if (B, C) may be executed (over-approximation)
    # There is an initial edge from None to the start block

    modified_flag: bool
    # Flag to check if we reach the fixpoint

    debug: bool
    # Print valueness and executability at each step if True

    all_vars: List[Operand]
    # All the variables of the CFG

    all_blocks: List[Block]
    # All the blocks of the CFG

    def __init__(self, cfg: CFG, debug: bool):
        self.cfg = cfg
        self.valueness = dict()
        self.executability = dict()
        self.debug = debug
        self.all_vars = list(cfg.gather_defs().keys())
        self.all_blocks = cfg.get_blocks()

        # Initialisation of valueness and executability
        for var in self.all_vars:
            self.valueness[var] = Lattice.Bottom
        for block in self.all_blocks:
            for succ in cfg.out_blocks(block):
                self.executability[block, succ] = False
        # Add an initial edge from None to the start block
        start_blk = self.cfg.get_block(self.cfg.get_start())
        self.executability[None, start_blk] = False

    def dump(self) -> None:  # pragma: no cover
        """
        For debug purposes: print valueness and executability.
        """
        print("Valueness:")
        for x, v in self.valueness.items():
            print("{0}: {1}".format(x, v))
        print("Executability:")
        for (B, C), v in self.executability.items():
            print("{0} -> {1}: {2}".format(B.get_label() if B is not None else "",
                                           C.get_label(), v))

    def set_valueness(self, v: Operand, x: LATTICE_VALUE) -> None:
        """
        Update the valueness of a variable `v` by performing a join with
        its current value.
        """
        old_x = self.valueness[v]
        new_x = join(x, old_x)
        if new_x != old_x:
            self.modified_flag = True
            self.valueness[v] = new_x

    def set_executability(self, B: Block | None, C: Block) -> None:
        """
        Mark the edge from `B` to `C` as executable.
        """
        old_x = self.executability[B, C]
        if not old_x:
            self.modified_flag = True
            self.executability[B, C] = True

    def is_constant(self, op: Operand) -> bool:
        """True if the value of `op` is constant."""
        return isinstance(self.valueness.get(op, None), int)

    def is_executable(self, B: Block) -> bool:
        """True if the block `B` may be executed."""
        return B in (C for ((_, C), b) in self.executability.items() if b)

    def compute(self) -> None:
        """
        Compute executability for all edges and valueness for all variables
        using a fixpoint algorithm.
        """
        # 1. For any v comming from outside the CFG (parameters, function calls),
        # set valueness[v] = Top. These are exactly the registers of A.
        for var in A:
            self.valueness[var] = Lattice.Top

        # 2. The start block is executable, with an initial edge coming from None.
        start_blk = self.cfg.get_block(self.cfg.get_start())
        self.set_executability(None, start_blk)

        # Start the fixpoint.
        self.modified_flag = True
        while self.modified_flag:
            # Whenever executability or valueness is modified,
            # modified_flag is set to True (see set_executability and set_valueness)
            # so that the fixpoint continues.
            self.modified_flag = False
            if self.debug:
                self.dump()

            # 3. For any executable block B with only one successor C,
            # set executability[B, C] = True.
            for B in self.all_blocks:
                nexts = self.cfg.out_blocks(B)
                if self.is_executable(B) and len(nexts) == 1:
                    C = nexts[0]
                    self.set_executability(B, C)

            for B in self.all_blocks:
                if self.is_executable(B):
                    for stat in B.get_all_statements():
                        self.propagate_in(B, stat)

    def propagate_in(self, B: Block, stat: Statement) -> None:
        """
        Propagate valueness and executability to the given statement `stat`
        located in the given executable block `B`.
        See the `compute` function for more context.
        """
        # 4. For any executable assignment v <- op (x, y),
        # set valueness[v] = eval (op, x, y)
        # TODO (Exercise 4)

        # 5. For any executable assignment v <- phi (x1, ..., xn),
        # set valueness[v] = join(x1, .., xn)
        # TODO (Exercise 6)

        # 6. For any executable conditional branch to blocks B1 and B2,
        # set executability[B1] = True and/or executability[B2] = True
        # depending on the valueness of its condition
        # TODO (Exercise 6)

    def get_executable_srcs(self, B: Block, phi: PhiNode) -> List[Operand]:
        """
        Given a phi node `phi` belonging to the block `B`,
        return its operands coming from an executable edge.
        """
        return [x for lbl, x in phi.used().items()
                if self.executability[self.cfg.get_block(lbl), B]]

    def get_operands(self, ins: Instruction) -> List[LATTICE_VALUE]:
        """
        Returns the valueness of the operands of the given instruction `ins`.
        Also takes into account immediate values and the zero register.
        """
        args: List[LATTICE_VALUE] = []
        all_used = ins.used()
        for x in all_used:
            if isinstance(x, Temporary):
                args.append(self.valueness[x])
            elif isinstance(x, Immediate):
                args.append(x._val)
            elif (x == ZERO):
                args.append(0)
            elif isinstance(x, Label):
                continue
            else:
                args.append(Lattice.Top)
        return args

    def eval_arith_instr(self, ins: Instruction) -> LATTICE_VALUE:
        """
        Computes the result of an arithmetic instruction in the valueness lattice,
        from the valueness of its operands.
        """
        args = self.get_operands(ins)
        name: str = ins.ins

        if has_top(args):
            return Lattice.Top
        elif has_bottom(args):
            return Lattice.Bottom

        args = cast(List[int], args)
        if name == "add" or name == "addi":
            return args[0] + args[1]
        elif name == "mul":
            return args[0] * args[1]
        elif name == "div":
            return div_rd_0(args[0], args[1])
        elif name == "rem":
            return mod_rd_0(args[0], args[1])
        elif name == "sub":
            return args[0] - args[1]
        elif name == "and":
            return args[0] & args[1]
        elif name == "or":
            return args[0] | args[1]
        elif name == "xor" or name == "xori":
            return args[0] ^ args[1]
        elif name == "li":
            assert (isinstance(ins.used()[0], Immediate))
            return args[0]
        elif name == "mv":
            return args[0]

        raise MiniCInternalError("Instruction modifying a temporary not in\
                                  ['add', 'addi', 'mul', 'div', 'rem',\
                                  'sub', 'and', 'or', 'xor', 'xori', 'li', 'mv']")

    def eval_bool_instr(self, ins: BranchingTerminator) -> LATTICE_VALUE:
        """
        Computes the result of the comparison of a branching instruction
        in the valueness lattice, from the valueness of its operands.
        """
        args = self.get_operands(ins)
        name: str = ins.ins

        if has_top(args):
            return Lattice.Top
        elif has_bottom(args):
            return Lattice.Bottom

        args = cast(List[int], args)
        if name == "blt":
            return args[0] < args[1]
        elif name == "bgt":
            return args[0] > args[1]
        elif name == "beq":
            return args[0] == args[1]
        elif name == "bne":
            return args[0] != args[1]
        elif name == "ble":
            return args[0] <= args[1]
        elif name == "bge":
            return args[0] >= args[1]
        elif name == "beqz":
            return args[0] == 0
        elif name == "bnez":
            return args[0] != 0

        raise MiniCInternalError("Condition of a CondJump not in ['blt',\
                                 'bgt', 'beq', 'bne', 'ble', 'bge',\
                                 'beqz', 'bnez']")

    def replacePhi(self, B: Block, ins: PhiNode) -> PhiNode:
        """
        Replace a phi node that has constant operands
        according to the valueness computation.
        """
        to_remove: List[Label] = []  # List of block's labels with no executable edge to B
        for Bi_label, xi in ins.used().items():
            Bi = self.cfg.get_block(Bi_label)
            if self.executability[Bi, B]:
                if self.is_constant(xi):
                    # Add a LI instruction in the block from where xi comes,
                    # at the end of its body (i.e. just before its Terminator),
                    # and replace xi by this new temporary
                    new_xi = self.cfg.fdata.fresh_tmp()
                    ins.srcs[Bi_label] = new_xi
                    imm = Immediate(self.valueness[xi])
                    li_ins = RiscV.li(new_xi, imm)
                    Bi.add_instruction(li_ins)
            else:
                to_remove.append(Bi_label)
        for Bi_label in to_remove:
            del ins.srcs[Bi_label]
        return ins

    def replaceInstruction(self, ins: BlockInstr) -> List[BlockInstr]:
        """
        Replace an instruction that has constant operands
        according to the valueness computation.
        """
        # Add some LI instructions before the instruction `ins`
        li_instrs: List[BlockInstr] = []
        # Replace the constant variables with the temporaries defined by the new LI instructions
        subst: Dict[Operand, Operand] = {}

        # Compute `li_instrs` and `subst`
        # TODO (Exercise 5)

        new_ins = ins.substitute(subst)
        return li_instrs + [new_ins]

    def replaceTerminator(self, ins: Terminator) -> Tuple[List[BlockInstr], Terminator]:
        """
        Replace a terminator that has constant operands
        according to the valueness computation.
        Return the list of LI instructions to do before,
        and the new terminator.
        """
        # Add some LI instructions at the end of the body of the block
        li_instrs: List[BlockInstr] = []
        # Replace the constant variables with the temporaries defined by the new LI instructions
        subst: Dict[Operand, Operand] = {}

        # Compute `li_instrs` and `subst`
        # TODO (Exercise 5)

        new_ins = ins.substitute(subst)
        return li_instrs, new_ins

    def rewriteCFG(self) -> None:
        """Update the CFG."""
        # a. Whenever executability[B, C] = False, delete this edge
        for (B, C) in [(B, C) for ((B, C), b) in self.executability.items()
                       if not b and B is not None]:
            # Remove the edge
            self.cfg.remove_edge(B, C)
            # Update the corresponding terminator
            targets = B.get_terminator().targets()
            targets.remove(C.get_label())
            if len(targets) == 0:
                B.set_terminator(Return())
            elif len(targets) == 1:
                B.set_terminator(AbsoluteJump(targets[0]))
            else:
                raise MiniCInternalError(
                    "rewriteCFG: A terminator has more than 2 targets: {}"
                    .format(targets + [C.get_label()]))
        # b. Whenever valueness[x] = c, substitute c for x and delete assignment to x
        for block in self.all_blocks:
            if self.is_executable(block):
                new_phis: List[PhiNode] = []
                for ins in block._phis:
                    assert (isinstance(ins, PhiNode))
                    v = ins.defined()[0]
                    if self.is_constant(v):
                        # We do not keep instructions defining operands of constant values
                        continue
                    else:
                        new_phis.append(self.replacePhi(block, ins))
                new_instrs: List[BlockInstr] = []
                for ins in block.get_body():
                    defs = ins.defined()
                    if len(defs) == 1 and self.is_constant(defs[0]):
                        # We do not keep instructions defining operands of constant values
                        continue
                    elif isinstance(ins, Instruction):
                        # We replace others instructions
                        new_instrs.extend(self.replaceInstruction(ins))
                    else:
                        # We do nothing for comments
                        new_instrs.append(ins)
                term_instrs, new_term = self.replaceTerminator(block.get_terminator())
                block._phis = cast(List[Statement], new_phis)
                block._instructions = new_instrs + term_instrs
                block.set_terminator(new_term)
        # c. Whenever a block B is not executable, delete B
        # There are no edge implicating B, for such an edge would not be executable,
        # whence would have been deleted beforehand
        for block in self.all_blocks:
            if not self.is_executable(block):
                del self.cfg._blocks[block.get_label()]


def OptimSSA(cfg: CFG, debug: bool) -> None:
    """Optimise a CFG under SSA form."""
    optim = CondConstantPropagation(cfg, debug)
    optim.compute()
    optim.rewriteCFG()
