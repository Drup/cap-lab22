#! /usr/bin/env python3

import os
import sys
import pytest
import glob
import subprocess
import re
from test_expect_pragma import (
    TestExpectPragmas, cat, testinfo,
    env_bool_variable, env_str_variable
    )

"""
Usage:
    python3 test_futur.py
(or make test)
"""

"""
CAP, 2020
Unit test infrastructure for testing futures:
1) compare the actual output to the expected one (in comments)
2) compare the actual output to the one obtained by simulation
"""

DISABLE_TYPECHECK = False
TYPECHECK_ONLY = False

HERE = os.path.dirname(os.path.realpath(__file__))
if HERE == os.path.realpath('.'):
    HERE = '.'
TEST_DIR = HERE
IMPLEM_DIR = HERE
MINIC_FUT = os.path.join(IMPLEM_DIR, 'MiniCC.py')

ALL_FILES = glob.glob(os.path.join(TEST_DIR,'tests/**/[a-zA-Z]*.c'), recursive=True)

GCC = 'gcc'

if 'TEST_FILES' in os.environ:
    ALL_FILES = glob.glob(os.environ['TEST_FILES'], recursive=True)


class TestFuture(TestExpectPragmas):

    # Not in test_expect_pragma to get assertion rewritting
    def assert_equal(self, actual, expected):
        if TYPECHECK_ONLY and expected.exitcode == 0:
            # Compiler does not fail => no output expected
            assert actual.output == "", \
                "Compiler unexpectedly generated some output with --disable-codegen"
            assert actual.exitcode == 0, \
                "Compiler unexpectedly failed with --disable-codegen"
            return
        if DISABLE_TYPECHECK and expected.exitcode != 0:
            # Test should fail at typecheck, and we don't do
            # typechecking => nothing to check.
            pytest.skip("Test that doesn't typecheck with --disable-typecheck")
        if expected.output is not None and actual.output is not None:
            assert actual.output == expected.output, \
                "Output of the program is incorrect."
        assert actual.exitcode == expected.exitcode, \
            "Exit code of the compiler is incorrect"
        assert actual.execcode == expected.execcode, \
            "Exit code of the execution is incorrect"

    def c2c(self, file):
        return self.run_command(['python3', MINIC_FUT, file])

    def compile_with_gcc(self, file, output_name):
        print("Compiling with GCC...")
        result = self.run_command(
            [GCC, '-Iinclude', '-Ilib', '-x', 'c', file, "lib/futurelib.c",
             '--output=' + output_name, '-lpthread'])
        print(result.output)
        print("Compiling with GCC... DONE")
        return result

    def compile_and_run(self, file):
        basename, _ = os.path.splitext(file)
        rw_name = basename + '.cfut'
        exec_name = basename + '.out'
        print("File: " + rw_name)
        resgcc = self.compile_with_gcc(rw_name, exec_name)
        if resgcc.exitcode != 0:
            return resgcc._replace(exitcode=1, output=None)
        res2 = self.run_command(exec_name, scope="runtime")
        return res2

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_future(self, filename):
        expect = self.get_expect(filename)
        c2csuccess = self.c2c(filename)
        if c2csuccess.exitcode == 0:
            actual = self.compile_and_run(filename)
        else:
            actual = c2csuccess
        self.assert_equal(actual, expect)


if __name__ == '__main__':
    pytest.main(sys.argv)
