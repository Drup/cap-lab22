import collections
import re
import os
import subprocess
import sys

testresult = collections.namedtuple('testresult', ['exitcode', 'output'])


def cat(filename):
    with open(filename, "rb") as f:
        for line in f:
            sys.stdout.buffer.write(line)


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

    def run_command(self, cmd):
        """Run the command cmd (given as [command, arg1, arg2, ...]), and
        return testresult(exitcode=..., output=...) containing the
        exit code of the command it its standard output + standard error.
        """
        try:
            output = subprocess.check_output(cmd, timeout=60,
                                             stderr=subprocess.STDOUT)
            exitcode = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exitcode = e.returncode
        return testresult(exitcode=exitcode, output=output.decode())

    __expect = {}

    def _extract_expect(self, file):
        exitcode = 0
        inside_expected = False
        expected_lines = []
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
                elif line == 'EXPECTED':
                    inside_expected = True
                elif inside_expected:
                    expected_lines.append(line)

        expected_lines.append('')
        return testresult(exitcode=exitcode,
                          output=os.linesep.join(expected_lines))
