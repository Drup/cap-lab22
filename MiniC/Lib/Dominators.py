"""
Utility functions to work with dominators in a :py:class:`CFG <Lib.CFG.CFG>`.

Do not hesitate to look at the source of the functions
to get a better understanding of the algorithms.
"""

from typing import Dict, Set
from graphviz import Digraph
from Lib.CFG import Block, CFG


def computeDom(cfg: CFG) -> Dict[Block, Set[Block]]:
    """
    `computeDom(cfg)` computes the table associating blocks to their
    dominators in `cfg`.
    It works by solving the equation system.

    This is an helper function called during SSA entry.
    """
    all_blocks: Set[Block] = set(cfg.get_blocks())
    dominators: Dict[Block, Set[Block]] = dict()
    for b in all_blocks:
        if b.get_in():  # If b has some predecessor
            dominators[b] = all_blocks
        else:  # If b has no predecessors
            dominators[b] = {b}
    new_dominators: Dict[Block, Set[Block]] = dict()
    while True:
        for b in all_blocks:
            if b.get_in():
                dom_preds = [dominators[b2] for b2 in b.get_in()]
                new_dominators[b] = {b}.union(set.intersection(*dom_preds))
            else:
                new_dominators[b] = {b}
        if dominators == new_dominators:
            break
        else:
            dominators = new_dominators
            new_dominators = dict()
    return dominators


def printDT(filename: str, graph: Dict[Block, Set[Block]]) -> None:  # pragma: no cover
    """Display a graphical rendering of the given domination tree."""
    dot = Digraph()
    for k in graph:
        dot.node(str(k.get_label()))
    for k in graph:
        for v in graph[k]:
            dot.edge(str(k.get_label()), str(v.get_label()))
    dot.render(filename, view=True)


def computeDT(cfg: CFG, dominators: Dict[Block, Set[Block]],
              dom_graphs: bool, basename: str) -> Dict[Block, Set[Block]]:
    """
    `computeDT(cfg, dominators)` computes the domination tree of `cfg`
    using the previously computed `dominators`.
    It returns `DT`, a dictionary which associates a block with its children
    in the dominator tree.

    This is an helper function called during SSA entry.
    """
    # First, compute the immediate dominators
    idominators: Dict[Block, Block] = {}
    for b, doms in dominators.items():
        # The immediate dominator of b is the unique vertex n ≠ b
        # which dominates b and is dominated by all vertices in Dom(b) − b.
        strict_doms = doms - {b}
        idoms = set()
        for n in strict_doms:
            if strict_doms.issubset(dominators[n]):
                idoms.add(n)
        if idoms:
            assert (len(idoms) == 1)
            idominators[b] = idoms.pop()
    # Then, simply inverse the relation to obtain the domination tree
    DT = {b: set() for b in cfg.get_blocks()}
    for i, idominator in idominators.items():
        DT[idominator].add(i)
    # Print the domination tree if asked
    if dom_graphs:
        s = "{}.{}.ssa.DT.dot".format(basename, cfg.fdata.get_name())
        print("SSA - domination tree graph:", s)
        printDT(s, DT)
    return DT


def _computeDF_at_block(
        cfg: CFG,
        dominators: Dict[Block, Set[Block]],
        DT: Dict[Block, Set[Block]],
        b: Block,
        DF: Dict[Block, Set[Block]]) -> None:
    """
    `_computeDF_at_block(...)` computes the dominance frontier at the given block,
    by updating `DF`.

    This is an helper function called during SSA entry.
    """
    S: Set[Block] = {succ for succ in cfg.out_blocks(b) if succ not in DT[b]}
    for b_succ in DT[b]:
        _computeDF_at_block(cfg, dominators, DT, b_succ, DF)
        for b_frontier in DF[b_succ]:
            if b not in (dominators[b_frontier] - {b_frontier}):
                S.add(b_frontier)
    DF[b] = S


def computeDF(cfg: CFG, dominators: Dict[Block, Set[Block]],
              DT: Dict[Block, Set[Block]], dom_graphs: bool, basename: str
              ) -> Dict[Block, Set[Block]]:
    """
    `computeDF(...)` computes the dominance frontier of a CFG.
    It returns `DF` which associates a block to its frontier.

    This is an helper function called during SSA entry.
    """
    DF: Dict[Block, Set[Block]] = dict()
    for b_entry in cfg.get_entries():
        _computeDF_at_block(cfg, dominators, DT, b_entry, DF)
    # Print the domination frontier on the CFG if asked
    if dom_graphs:
        s = "{}.{}.ssa.DF.dot".format(basename, cfg.fdata.get_name())
        print("SSA - dominance frontier graph:", s)
        cfg.print_dot(s, DF, True)
    return DF
