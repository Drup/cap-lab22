#! /usr/bin/env python3
"""
Code generation lab, main file. Code Generation with Smart IRs.
Usage:
    python3 MiniCC.py <filename>
    python3 MiniCC.py --help
"""
import traceback
from typing import cast
from MiniCLexer import MiniCLexer
from MiniCParser import MiniCParser
from TP03.MiniCTypingVisitor import MiniCTypingVisitor, MiniCTypeError
from TP03.MiniCInterpretVisitor import MiniCInterpretVisitor
from Lib.Errors import (MiniCUnsupportedError, MiniCInternalError,
                        MiniCRuntimeError, AllocationError)

from enum import Enum
import argparse

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

import os
import sys


class Mode(Enum):
    PARSE = 0
    EVAL = 1
    LINEAR = 2
    CFG = 3
    SSA = 4
    OPTIM = 5

    def is_codegen(self) -> bool:
        return self.value >= Mode.LINEAR.value


def valid_modes():
    modes = ['parse', 'typecheck', 'eval']

    try:
        import TP04.MiniCCodeGen3AVisitor  # type: ignore[import]
        modes.append('codegen-linear')
    except ImportError:
        return modes

    try:
        import Lib.CFG  # type: ignore[import]
        modes.append('codegen-cfg')
    except ImportError:
        return modes

    try:
        import TP05.SSA  # type: ignore[import]
        modes.append('codegen-ssa')
    except ImportError:
        return modes

    try:
        import TP05c.OptimSSA  # type: ignore[import]
        modes.append('codegen-optim')
    except ImportError:
        pass

    return modes


class CountErrorListener(ErrorListener):
    """Count number of errors.

    Parser provides getNumberOfSyntaxErrors(), but the Lexer
    apparently doesn't provide an easy way to know if an error occurred
    after the fact. Do the counting ourserves with a listener.
    """

    def __init__(self):
        super(CountErrorListener, self).__init__()
        self.count = 0

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        self.count += 1


def main(inputname, reg_alloc, mode,
         typecheck=True, stdout=False, output_name=None, debug=False,
         debug_graphs=False, ssa_graphs=False):
    (basename, rest) = os.path.splitext(inputname)
    if mode.is_codegen():
        if stdout:
            output_name = None
            print("Code will be generated on standard output")
        elif output_name is None:
            output_name = basename + ".s"
            print("Code will be generated in file " + output_name)

    input_s = FileStream(inputname, encoding='utf-8')
    lexer = MiniCLexer(input_s)
    counter = CountErrorListener()
    lexer._listeners.append(counter)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    parser._listeners.append(counter)
    tree = parser.prog()
    if counter.count > 0:
        exit(3)  # Syntax or lexicography errors occurred, don't try to go further.
    if typecheck:
        typing_visitor = MiniCTypingVisitor()
        try:
            typing_visitor.visit(tree)
        except MiniCTypeError as e:
            print(e.args[0])
            exit(2)

    if mode == Mode.EVAL:
        # interpret Visitor
        interpreter_visitor = MiniCInterpretVisitor()
        try:
            interpreter_visitor.visit(tree)
        except MiniCRuntimeError as e:
            print(e.args[0])
            exit(1)
        except MiniCInternalError as e:
            print(e.args[0], file=sys.stderr)
            exit(4)
        return

    if not mode.is_codegen():
        if debug:
            print("Not running code generation because of --typecheck-only.")
        return

    # Codegen 3@ CFG Visitor, first argument is debug mode
    from TP04.MiniCCodeGen3AVisitor import MiniCCodeGen3AVisitor  # type: ignore[import]
    visitor3 = MiniCCodeGen3AVisitor(debug, parser)

    # dump generated code on stdout or file.
    with open(output_name, 'w') if output_name else sys.stdout as output:
        visitor3.visit(tree)
        for function in visitor3.get_functions():
            fdata = function.fdata
            # Allocation part
            if mode == Mode.LINEAR:
                code = function
            else:
                from TP04.BuildCFG import build_cfg  # type: ignore[import]
                from Lib.CFG import CFG  # type: ignore[import]
                code = build_cfg(function)
                assert(isinstance(code, CFG))
            if debug_graphs:
                s = "{}.{}.dot".format(basename, code.fdata._name)
                print("CFG:", s)
                code.print_dot(s, view=True)
            if mode.value >= Mode.SSA.value:
                from TP05.SSA import enter_ssa  # type: ignore[import]
                from Lib.CFG import CFG  # type: ignore[import]

                DF = enter_ssa(cast(CFG, code), basename, debug, ssa_graphs)
                if ssa_graphs:
                    s = "{}.{}.ssa.dot".format(basename, code.fdata._name)
                    print("SSA:", s)
                    code.print_dot(s, DF, True)
                if mode == Mode.OPTIM:
                    from TP05c.OptimSSA import OptimSSA  # type: ignore[import]
                    OptimSSA(cast(CFG, code), debug=debug)
                    if ssa_graphs:
                        s = "{}.{}.optimssa.dot".format(basename, code.fdata._name)
                        print("SSA after optim:", s)
                        code.print_dot(s, view=True)
            allocator = None
            if reg_alloc == "naive":
                from Lib.Allocator import NaiveAllocator  # type: ignore[import]
                allocator = NaiveAllocator(fdata)
                comment = "naive allocation"
            elif reg_alloc == "all-in-mem":
                from TP04.AllInMemAllocator import AllInMemAllocator  # type: ignore[import]
                allocator = AllInMemAllocator(fdata)
                comment = "all-in-memory allocation"
            elif reg_alloc == "smart":
                liveness = None
                if mode == Mode.SSA:
                    from TP05.LivenessSSA import LivenessSSA  # type: ignore[import]
                    try:
                        from Lib.CFG import CFG  # type: ignore[import]
                        liveness = LivenessSSA(cast(CFG, code), debug=debug)
                    except NameError:
                        form = "CFG in SSA form"
                        raise ValueError("Invalid dataflow form: \
liveness file not found for {}.".format(form))
                else:
                    try:
                        from TP05.LivenessDataFlow import LivenessDataFlow  # type: ignore[import]
                        liveness = LivenessDataFlow(code, debug=debug)
                    except NameError:
                        form = "CFG not in SSA form"
                        raise ValueError("Invalid dataflow form: \
liveness file not found for {}.".format(form))
                from TP05.SmartAllocator import SmartAllocator  # type: ignore[import]
                allocator = SmartAllocator(fdata, basename, liveness,
                                           debug, debug_graphs)
                comment = "smart allocation with graph coloring"
            elif reg_alloc == "none":
                comment = "non executable 3-Address instructions"
            else:
                raise ValueError("Invalid allocation strategy:" + reg_alloc)
            if allocator:
                allocator.prepare()
            if mode == Mode.SSA:
                from Lib.CFG import CFG  # type: ignore[import]
                from TP05.SSA import exit_ssa  # type: ignore[import]
                exit_ssa(cast(CFG, code))
                comment += " with SSA"
            if allocator:
                allocator.rewriteCode(code)
            if mode == Mode.SSA and ssa_graphs:
                s = "{}.{}.exitssa.dot".format(basename, code.fdata._name)
                print("CFG after SSA:", s)
                code.print_dot(s, view=True)
            code.print_code(output, comment=comment)
            if debug:
                visitor3.printSymbolTable()


# command line management
if __name__ == '__main__':

    modes = valid_modes()

    parser = argparse.ArgumentParser(description='Generate code for .c file')

    parser.add_argument('filename', type=str,
                        help='Source file.')
    parser.add_argument('--mode', type=str,
                        choices=valid_modes(),
                        required=True,
                        help='Operation to perform on the input program')
    parser.add_argument('--debug', action='store_true',
                        default=False,
                        help='Emit verbose debug output')
    parser.add_argument('--disable-typecheck', action='store_true',
                        default=False,
                        help="Don't run the typechecker before evaluation or code generation")

    if "codegen-linear" in modes:
        parser.add_argument('--reg-alloc', type=str,
                            choices=['none', 'naive', 'all-in-mem', 'smart'],
                            help='Register allocation to perform during code generation')
        parser.add_argument('--stdout', action='store_true',
                            help='Generate code to stdout')
        parser.add_argument('--output', type=str,
                            help='Generate code to outfile')

    if "codegen-cfg" in modes:
        parser.add_argument('--graphs', action='store_true',
                            default=False,
                            help='Display graphs (CFG, conflict graph).')

    if "codegen-ssa" in modes:
        parser.add_argument('--ssa-graphs', action='store_true',
                            default=False,
                            help='Display SSA graphs (DT, DF).')

    args = parser.parse_args()
    reg_alloc = args.reg_alloc if "codegen-linear" in modes else None
    to_stdout = args.stdout if "codegen-linear" in modes else False
    outfile = args.output if "codegen-linear" in modes else None
    graphs = args.graphs if "codegen-cfg" in modes else False
    ssa_graphs = args.ssa_graphs if "codegen-ssa" in modes else False

    if reg_alloc is None and "codegen" in args.mode:
        print("error: the following arguments is required: --reg-alloc")
        exit(1)
    elif reg_alloc is not None and "codegen" not in args.mode:
        print("error: register allocation is only available in code generation mode")
        exit(1)

    typecheck = not args.disable_typecheck

    if args.mode == "parse":
        mode = Mode.PARSE
        typecheck = False
    elif args.mode == "typecheck":
        mode = Mode.PARSE
    elif args.mode == "eval":
        mode = Mode.EVAL
    elif args.mode == "codegen-linear":
        mode = Mode.LINEAR
        if reg_alloc == "smart":
            print("error: smart register allocation is not compatible with linear code generation")
            exit(1)
    elif args.mode == "codegen-cfg":
        mode = Mode.CFG
    elif args.mode == "codegen-ssa":
        mode = Mode.SSA
    elif args.mode == "codegen-optim":
        mode = Mode.OPTIM
    else:
        raise ValueError("Invalid mode:" + args.mode)

    try:
        main(args.filename, reg_alloc, mode,
             typecheck,
             to_stdout, outfile, args.debug,
             graphs, ssa_graphs)
    except MiniCUnsupportedError as e:
        print(e)
        exit(5)
    except (MiniCInternalError, AllocationError):
        traceback.print_exc()
        exit(4)
