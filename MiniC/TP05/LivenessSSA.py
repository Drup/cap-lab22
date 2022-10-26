from typing import Dict, Set, Tuple
from Lib.Operands import Temporary
from Lib.Statement import Statement, regset_to_string
from Lib.CFG import Block, CFG
from Lib.PhiNode import PhiNode


class LivenessSSA:
    """Liveness Analysis on a CFG under SSA Form."""

    def __init__(self, cfg: CFG, debug=False):
        self._cfg: CFG = cfg
        self._debug: bool = debug
        # Temporary already propagated, by Block
        self._seen: Dict[Block, Set[Temporary]] = dict()
        # Live Temporary at outputs of Statement
        self._liveout: Dict[Statement, Set[Temporary]] = dict()

    def run(self) -> None:
        """Compute the liveness."""
        # Initialization
        for block in self._cfg.get_blocks():
            self._seen[block] = set()
            for instr in block.get_all_statements():
                self._liveout[instr] = set()
        # Start the use-def chains
        for var, uses in self.gather_uses().items():
            for block, pos, instr in uses:
                self.live_start(block, pos, instr, var)
        # Add conflicts on phis
        self.conflict_on_phis()
        # Final debugging print
        if self._debug:
            self.print_map_in_out()

    def live_start(self, block: Block, pos: int | None,
                   s: Statement, var: Temporary) -> None:
        """Start backward propagation of liveness information."""
        if isinstance(s, PhiNode):
            assert(pos is None)
            for label, var_phi in s.used().items():
                if var_phi == var:
                    prev_block = self._cfg.get_block(label)
                    self.liveout_at_block(prev_block, var)
        else:
            assert(pos is not None)
            self.livein_at_instruction(block, pos, var)

    def liveout_at_block(self, block: Block, var: Temporary) -> None:
        """Backward propagation of liveness information at a block."""
        raise NotImplementedError("LivenessSSA") # TODO (Lab 5b, Exercise 1)

    def liveout_at_instruction(self, block: Block, pos: int, var: Temporary) -> None:
        """Backward propagation of liveness information at a non-phi instruction."""
        instr = block.get_body_and_terminator()[pos]
        raise NotImplementedError("LivenessSSA") # TODO (Lab 5b, Exercise 1)

    def livein_at_instruction(self, block: Block, pos: int, var: Temporary) -> None:
        """Backward propagation of liveness information at a non-phi instruction."""
        raise NotImplementedError("LivenessSSA") # TODO (Lab 5b, Exercise 1)

    def gather_uses(self) -> Dict[Temporary, Set[Tuple[Block, int | None, Statement]]]:
        """
        Return a dictionnary giving for each variable the set of statements using it,
        with additionnaly for each statement, the block of the statement and its position inside.
        Phi instructions have position None in their block, while a Terminaor is at the last
        position of its block.
        """
        uses: Dict[Temporary, Set[Tuple[Block, int | None, Statement]]] = dict()
        for block in self._cfg.get_blocks():
            # Look inside the phi node
            for instr in block._phis:
                assert (isinstance(instr, PhiNode))
                for var in instr.used().values():
                    if isinstance(var, Temporary):
                        var_uses = uses.get(var, set())
                        uses[var] = var_uses.union({(block, None, instr)})
            # Look inside the body and the terminator
            for pos, instr in enumerate(block.get_body_and_terminator()):
                for var in instr.used():
                    if isinstance(var, Temporary):
                        var_uses = uses.get(var, set())
                        uses[var] = var_uses.union({(block, pos, instr)})
        return uses

    def conflict_on_phis(self) -> None:
        """Ensures that variables defined by phi instructions are in conflict with one-another."""
        raise NotImplementedError("LivenessSSA") # TODO (Lab 5b, Exercise 1)

    def print_map_in_out(self) -> None:  # pragma: no cover
        """Print live out sets at each instruction, group by block, useful for debugging!"""
        print("Liveout: [")
        for block in self._cfg.get_blocks():
            print("Block " + str(block.get_label()) + ": {\n "
                  + ",\n ".join("\"{}\": {}"
                  .format(instr, regset_to_string(self._liveout[instr]))
                  for instr in block.get_all_statements()) +
                  "}")
        print("]")
