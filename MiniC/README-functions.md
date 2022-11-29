# MiniC Compiler 
LAB6 (code generation for functions), MIF08 / CAP 2022-23

# Authors

YOUR NAME HERE

# Contents

TODO: Say a bit about the code infrastructure ...

# Howto

As in the previous labs.

`make test-codegen SSA=1` to lauch pyright and the testsuite
with the three allocators (do not forget the options you can add).

# Test design 

TODO: give the main objectives of your tests.

# Design choices

TODO: explain your choices

# Known bugs

TODO: bugs and limitations you could not fix (if any).

# Checklists

A check ([X]) means that the feature is implemented 
and *tested* with appropriate test cases.

## Parser

- [ ] Function definition
- [ ] Function declaration
- [ ] Function call

## Typer

- [ ] Function declaration
- [ ] Function definition
- [ ] Function call
- [ ] Function return

## Code generation

- [ ] Function return
- [ ] Callee-saved registers
- [ ] Function call
- [ ] Getting the result of a function call
- [ ] Caller-saved registers
- [ ] Increase the size of the stack for callee/caller-saved registers
- [ ] Temporaries for giving arguments to a function call
- [ ] Temporaries for retriving arguments at the beginning of a function


