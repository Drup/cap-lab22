import collections
import re
import os
import subprocess
import sys
import pytest

testinfo = collections.namedtuple(
    'testinfo',
    ['exitcode', 'execcode', 'output', 'linkargs', 'skip_test_expected'])
default_testinfo = testinfo(
    exitcode=0, execcode=0, output='', linkargs=[], skip_test_expected=False)


def cat(filename):
    with open(filename, "rb") as f:
        for line in f:
            sys.stdout.buffer.write(line)


def env_bool_variable(name, globals):
    if name not in globals:
        globals[name] = False
    if name in os.environ:
        globals[name] = True


def env_str_variable(name, globals):
    if name in os.environ:
        globals[name] = os.environ[name]


class TestExpectPragmas(object):
    """Base class for tests that read the expected result as annotations
    in test files.

    get_expect(file) will parse the file, looking EXPECT and EXITCODE
    pragmas.

    run_command(command) is a wrapper around subprocess.check_output()
    that extracts the output and exit code.

    """

    def get_expect(self, filename):
        """Parse "filename" looking for EXPECT and EXITCODE annotations.

        Look for a line "EXPECTED" (possibly with whitespaces and
        comments). Text after this "EXPECTED" line is the expected
        output.

        The file may also contain a line like "EXITCODE <n>" where <n>
        is an integer, and is the expected exitcode of the command.

        The result is cached to avoid re-parsing the file multiple
        times.
        """
        if filename not in self.__expect:
            self.__expect[filename] = self._extract_expect(filename)
        return self.__expect[filename]

    def remove(self, file):
        """Like os.remove(), but ignore errors, e.g. don't complain if the
        file doesn't exist.
        """
        try:
            os.remove(file)
        except OSError:
            pass

    def run_command(self, cmd, scope="compile"):
        """Run the command cmd (given as [command, arg1, arg2, ...]), and
        return testinfo(exitcode=..., output=...) containing the
        exit code of the command it its standard output + standard error.

        If scope="compile" (resp. "runtime"), then the exitcode (resp.
        execcode) is set with the exit status of the command, and the
        execcode (resp. exitcode) is set to 0.
        """
        try:
            output = subprocess.check_output(cmd, timeout=60,
                                             stderr=subprocess.STDOUT)
            status = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            status = e.returncode
        if scope == "runtime":
            return default_testinfo._replace(execcode=status,
                                             output=output.decode())
        else:
            return default_testinfo._replace(exitcode=status,
                                             output=output.decode())

    def skip_if_partial_match(self, actual, expect, ignore_error_message):
        if not ignore_error_message:
            return False

        # TODO: Deal with undefined behavior here?

        if expect.exitcode != actual.exitcode:
            # Not the same exit code => something's wrong anyway
            return False

        if actual.exitcode == 3:
            # There's a syntax error in both expected and actual,
            # but the actual error may slightly differ if we don't
            # have the exact same .g4.
            return True

        # Let the test pass with 'return True' if appropriate.
        # Otherwise, continue to the full assertion for a
        # complete diagnostic.
        if actual.exitcode != 0 and expect.exitcode == actual.exitcode:
            if expect.output == '':
                # No output expected, but we know there must be an
                # error. If there was a particular error message
                # expected, we'd have written it in the output,
                # hence just ignore the actual message.
                return True
            # Ignore difference in error message except in the
            # line number (ignore the column too, it may
            # slightly vary, eg. in "foo" / 4, the error may
            # be considered on "foo" or on /):
            if re.match(r'^In function [^ :]*: Line [0-9]* col [0-9]*:', actual.output):
                out_loc = re.sub(r' col [0-9]*:.*$', '', actual.output)
                exp_loc = re.sub(r' col [0-9]*:.*$', '', expect.output)
                if out_loc == exp_loc:
                    return True
            if any(x.output and (x.output.endswith('has no value yet!' + os.linesep)
                                 or x.output.endswith(' by 0' + os.linesep))
                   for x in (actual, expect)):
                # Ignore the error message when our compiler
                # raises this error (either in actual or expect,
                # depending on what we're testing).
                return True

        return False

    __expect = {}

    def _extract_expect(self, file):
        exitcode = 0
        execcode = 0
        linkargs = []
        inside_expected = False
        skip_test_expected = False
        expected_lines = []
        expected_present = False
        with open(file, encoding="utf-8") as f:
            for line in f.readlines():
                # Ignore non-comments
                if not re.match(r'\s*//', line):
                    continue
                # Cleanup comment start and whitespaces
                line = re.sub(r'\s*//\s*', '', line)
                line = re.sub(r'\s*$', '', line)

                if line == 'END EXPECTED':
                    inside_expected = False
                elif line.startswith('EXITCODE'):
                    words = line.split(' ')
                    assert len(words) == 2
                    exitcode = int(words[1])
                elif line.startswith('EXECCODE'):
                    words = line.split(' ')
                    assert len(words) == 2
                    execcode = int(words[1])
                elif line.startswith('LINKARGS'):
                    words = line.split(' ')
                    assert len(words) >= 2
                    linkargs += [w.replace("$dir", os.path.dirname(file))
                                 for w in words[1:]]
                elif line == 'EXPECTED':
                    inside_expected = True
                    expected_present = True
                elif line == 'SKIP TEST EXPECTED':
                    skip_test_expected = True
                elif inside_expected:
                    expected_lines.append(line)

        if not expected_present:
            pytest.fail("Missing EXPECTED directive in test file")

        if expected_lines == []:
            output = ''
        else:
            output = os.linesep.join(expected_lines) + os.linesep

        return testinfo(exitcode=exitcode, execcode=execcode,
                        output=output, linkargs=linkargs,
                        skip_test_expected=skip_test_expected)
