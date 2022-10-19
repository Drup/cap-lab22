.. MiniC documentation master file, created by
   sphinx-quickstart on Thu Feb  3 16:47:38 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MiniC's documentation!
=================================

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   Base library - Errors <api/Lib.Errors>
   Base library - Statement <api/Lib.Statement>
   Base library - RISC-V instructions <api/Lib.RiscV>
   Base library - Operands <api/Lib.Operands>
   Base library - Function data <api/Lib.FunctionData>
   Base library - Graphs <api/Lib.Graphes>
   Linear intermediate representation <api/Lib.LinearCode>
   Temporary allocation <api/Lib.Allocator>
   Control Flow Graph - CFG and Basic blocks <api/Lib.CFG>
   Control Flow Graph - Terminators <api/Lib.Terminator>
   SSA form - Dominance frontier <api/Lib.Dominators>
   SSA form - Phi Nodes <api/Lib.PhiNode>

These pages document the various Python sources in the Lib/
folder of MiniC. You should not have to edit them *at all*.

Base library
------------

The :doc:`api/Lib.Statement` defines various classes that represent
RISC-V assembly statements, such as labels or 3-address instructions.

We won't create objects of these classes directly very often.
Instead, to easily create such statements for standard RISC-V assembly instructions
and pseudo-instructions, we give you the :doc:`api/Lib.RiscV`.

RISC-V instructions take arguments of various kinds,
as defined in the :doc:`api/Lib.Operands`.

At some point, we will need some basic functions about oriented and non oriented graphs,
those are present in :doc:`api/Lib.Graphes`.

Linear Intermediate representation
----------------------------------

The :doc:`api/Lib.LinearCode` allows to work with assembly source code
modeled as a list of statements.

Temporary allocation
--------------------

Before implementing the all-in-memory allocator of lab 4a,
you should understand the naive allocator in the :doc:`api/Lib.Allocator`.

Control Flow Graph Intermediate representation
----------------------------------------------

The classes for the CFG and its basic blocks are in the :doc:`api/Lib.CFG`.
Each block ends with a terminator, as documented in the :doc:`api/Lib.Terminator`.

SSA form
--------

The translation of the CFG into SSA form makes use of dominance frontiers.
Functions to work with dominance are defined in the :doc:`api/Lib.Dominators`.

Phi nodes, a special kind of statement that appears in CFGs in SSA form,
are defined in the :doc:`api/Lib.PhiNode`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
