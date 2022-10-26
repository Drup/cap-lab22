from typing import List, Set, Tuple
from Lib import RiscV
from Lib.Graphes import DiGraph
from Lib.CFG import BlockInstr
from Lib.Operands import (Register, DataLocation, S)


def generate_smart_move(dest: DataLocation, src: DataLocation) -> List[BlockInstr]:
    """
    Generate a list of move, store and load instructions, depending if the
    operands are registers or memory locations.
    This is an helper function for `sequentialize_moves`.
    """
    instr: List[BlockInstr] = []
    # TODO Compute the moves (Lab 5b, Exercise 4)
    raise NotImplementedError("generate_smart_move")
    return instr


def sequentialize_moves(parallel_moves: Set[Tuple[DataLocation, DataLocation]]
                        ) -> List[BlockInstr]:
    """
    Take a set of parallel moves represented as (destination, source) pairs,
    and return a list of sequential moves which respect the cycles.
    Use the register `tmp` S2 for the cycles.
    Return a corresponding list of RiscV instructions.
    This is an helper function called during SSA exit.
    """
    tmp: Register = S[2]  # S2 is not a general purpose register
    # Build the graph of the moves
    move_graph: DiGraph = DiGraph()
    for dest, src in parallel_moves:
        move_graph.add_edge((src, dest))
    # List for the sequentialized moves to do
    # Convention: in moves we put (dest, src) for each move
    moves: List[Tuple[DataLocation, DataLocation]] = []
    # First iteratively remove all the vetices without successors
    vars_without_successor = {src
                              for src, dests in move_graph.neighbourhoods()
                              if len(dests) == 0}
    while vars_without_successor:
        # TODO Remove the leaves iteratively (Lab 5b, Exercise 4)
        raise NotImplementedError("sequentialize_moves: leaves")
    # Then handle the cycles
    cycles: List = move_graph.connected_components()
    for cycle in cycles:
        # TODO Handle each cycle (Lab 5b, Exercise 4)
        raise NotImplementedError("sequentialize_moves: cycles")
    # Transform the moves to do in actual RiscV instructions
    moves_instr: List[BlockInstr] = []
    for dest, src in moves:
        instrs = generate_smart_move(dest, src)
        moves_instr.extend(instrs)
    return moves_instr
