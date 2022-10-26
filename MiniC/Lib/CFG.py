"""
Classes for a RiscV CFG: :py:class:`CFG` for the CFG itself,
and :py:class:`Block` for its basic blocks.
"""

from graphviz import Digraph  # for dot output
from typing import cast, Any, Dict, List, Set, Iterator

from Lib.Errors import MiniCInternalError
from Lib.Operands import (Operand, Immediate, Function, A0)
from Lib.Statement import (
    Statement, Instru3A, Label,
    AbsoluteJump, ConditionalJump, Comment
)
from Lib.Terminator import (
    Terminator, BranchingTerminator, Return)
from Lib.FunctionData import (FunctionData, _iter_statements, _print_code)


BlockInstr = Instru3A | Comment


class Block:
    """
    A basic block of a :py:class:`CFG` is made of three main parts:

    - a start :py:class:`label <Lib.Statement.Label>` that uniquely identifies the block in the CFG
    - the main body of the block, a list of instructions
      (excluding labels, jumps and branching instructions)
    - a :py:class:`terminator <Lib.Terminator.Terminator>`
      that represents the final jump or branching instruction of the block,
      and points to the successors of the block.
      See the documentation for :py:class:`Lib.Terminator.Terminator` for further explanations.
    """

    _terminator: Terminator
    _label: Label
    _phis: List[Statement]
    _instructions: List[BlockInstr]
    _in: List['Block']
    _gen: Set
    _kill: Set

    def __init__(self, label: Label, insts: List[BlockInstr], terminator: Terminator):
        self._label = label
        self._instructions = insts
        self._in = []
        self._phis = []
        self._terminator = terminator
        self._gen = set()
        self._kill = set()

    def __str__(self):
        instr = [i for i in self._instructions if not isinstance(i, Comment)]
        instr_str = '\n'.join(map(str, instr))
        s = '{}:\n\n{}'.format(self._label, instr_str)
        return s

    def to_dot(self) -> str:  # pragma: no cover
        """Outputs all statements of the block as a string."""
        # dot is weird: lines ending with \l instead of \n are left-aligned.
        NEWLINE = '\\l    '
        instr = []
        instr += self._phis
        instr += [i for i in self._instructions if not isinstance(i, Comment)]
        instr += [self.get_terminator()]
        instr_str = NEWLINE.join(map(str, instr))
        s = '{}:{}{}\\l'.format(self._label, NEWLINE, instr_str)
        return s

    def __repr__(self):
        return str(self._label)

    def get_body(self) -> List[BlockInstr]:
        """Return the statements in the body of the block (no phi-node nor the terminator)."""
        return self._instructions

    def get_all_statements(self) -> List[Statement]:
        """
        Return all statements of the block
        (including phi-nodes and the terminator, but not the label of the block).
        """
        return (self._phis +
                cast(List[Statement], self._instructions) +
                [self.get_terminator()])

    def get_body_and_terminator(self) -> List[Statement]:
        """
        Return all statements of the block, except phi-nodes
        (and the label of the block).
        """
        return (cast(List[Statement], self._instructions) +
                [self.get_terminator()])

    def get_label(self) -> Label:
        """Return the label of the block."""
        return self._label

    def get_in(self) -> List['Block']:
        """Return the list of blocks with an edge to the considered block."""
        return self._in

    def get_terminator(self) -> Terminator:
        """Return the terminator of the block."""
        return self._terminator

    def set_terminator(self, term: Terminator) -> None:
        """Set the terminator of the block."""
        self._terminator = term

    def iter_statements(self, f) -> None:
        """Iterate over instructions.
        For each real instruction i (not label or comment), replace it
        with the list of instructions given by f(i).

        Assume there is no phi-node.
        """
        assert (self._phis == [])
        new_statements = _iter_statements(self._instructions, f)
        end_statements = f(self.get_terminator())
        if len(end_statements) >= 1 and isinstance(end_statements[-1], Terminator):
            new_terminator = end_statements.pop(-1)
            self._instructions = new_statements + end_statements
            self.set_terminator(new_terminator)
        else:
            raise MiniCInternalError(
                "Block.iter_statements: Invalid replacement for terminator {}:\n {}"
                .format(self.get_terminator(), end_statements))

    def add_instruction(self, instr: BlockInstr) -> None:
        """Add an instruction to the body of the block."""
        self._instructions.append(instr)


class CFG:
    """
    A complete control-flow graph representing a function.
    This class is mainly made of a list of basic :py:class:`Block`,
    a label indicating the :py:meth:`entry point of the function <get_start>`,
    and an :py:meth:`exit label <get_end>`.

    As with linear code, metadata about the function can be found
    in the :py:attr:`fdata` member variable.
    """

    _start: Label
    _end: Label
    _blocks: Dict[Label, Block]

    #: Metadata about the function represented by this CFG
    fdata: FunctionData

    def __init__(self, fdata: FunctionData):
        self._blocks = {}
        self.fdata = fdata
        self._init_blks()
        self._end = self.fdata.fresh_label("end")

    def _init_blks(self) -> None:
        """Add a block for division by 0."""
        # Label for the address of the error message
        # This address is added by print_code
        label_div_by_zero_msg = Label(self.fdata._label_div_by_zero.name + "_msg")
        blk = Block(self.fdata._label_div_by_zero, [
            Instru3A("la", A0, label_div_by_zero_msg),
            Instru3A("call", Function("println_string")),
            Instru3A("li", A0, Immediate(1)),
            Instru3A("call", Function("exit")),
        ], terminator=Return())
        self.add_block(blk)

    def get_start(self) -> Label:
        """Return the entry label of the CFG."""
        return self._start

    def set_start(self, start: Label) -> None:
        """Set the entry label of the CFG."""
        assert (start in self._blocks)
        self._start = start

    def get_end(self) -> Label:
        """Return the exit label of the CFG."""
        return self._end

    def add_block(self, blk: Block) -> None:
        """Add a new block to the CFG."""
        self._blocks[blk._label] = blk

    def get_block(self, name: Label) -> Block:
        """Return the block with label `name`."""
        return self._blocks[name]

    def get_blocks(self) -> List[Block]:
        """Return all the blocks."""
        return [b for b in self._blocks.values()]

    def get_entries(self) -> List[Block]:
        """Return all the blocks with no predecessors."""
        return [b for b in self._blocks.values() if not b.get_in()]

    def add_edge(self, src: Block, dest: Block) -> None:
        """Add the edge src -> dest in the control flow graph."""
        dest.get_in().append(src)
        # assert (dest.get_label() in src.get_terminator().targets())

    def remove_edge(self, src: Block, dest: Block) -> None:
        """Remove the edge src -> dest in the control flow graph."""
        dest.get_in().remove(src)
        # assert (dest.get_label() not in src.get_terminator().targets())

    def out_blocks(self, block: Block) -> List[Block]:
        """
        Return the list of blocks in the CFG targeted by
        the Terminator of Block block.
        """
        return [self.get_block(dest) for dest in block.get_terminator().targets()]

    def gather_defs(self) -> Dict[Any, Set[Block]]:
        """
        Return a dictionary associating variables to all the blocks
        containing one of their definitions.
        """
        defs: Dict[Operand, Set[Block]] = dict()
        for b in self.get_blocks():
            for i in b.get_all_statements():
                for v in i.defined():
                    if v not in defs:
                        defs[v] = {b}
                    else:
                        defs[v].add(b)
        return defs

    def iter_statements(self, f) -> None:
        """Apply f to all instructions in all the blocks."""
        for b in self.get_blocks():
            b.iter_statements(f)

    def linearize_naive(self) -> Iterator[Statement]:
        """
        Linearize the given control flow graph as a list of instructions.
        Naive procedure that adds jumps everywhere.
        """
        for label, block in self._blocks.items():
            yield label
            for i in block._instructions:
                yield i
            match block.get_terminator():
                case BranchingTerminator() as j:
                    # In case of conditional jump, add the missing edge
                    yield ConditionalJump(j.cond, j.op1, j.op2, j.label_then)
                    yield AbsoluteJump(j.label_else)
                case AbsoluteJump() as j:
                    yield AbsoluteJump(j.label)
                case Return():
                    yield AbsoluteJump(self.get_end())

    def print_code(self, output, linearize=(lambda cfg: list(cfg.linearize_naive())),
                   comment=None) -> None:
        """Print the linearization of the CFG."""
        statements = linearize(self)
        _print_code(statements, self.fdata, output, init_label=self._start,
                    fin_label=self._end, fin_div0=False, comment=comment)

    def print_dot(self, filename, DF=None, view=False) -> None:  # pragma: no cover
        """Print the CFG as a graph."""
        graph = Digraph()
        # nodes
        for name, blk in self._blocks.items():
            if DF is not None:
                df_str = "{}" if blk not in DF or not len(DF[blk]) else str(DF[blk])
                df_lab = blk.to_dot() + "\n\nDominance frontier:\n" + df_str
            else:
                df_lab = blk.to_dot()
            graph.node(str(blk._label), label=df_lab, shape='rectangle')
        # edges
        for name, blk in self._blocks.items():
            for child in blk.get_terminator().targets():
                graph.edge(str(blk._label), str(child))
        graph.render(filename, view=view)
