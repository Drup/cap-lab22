# Simplest way: binary installation

A pre-compiled archive is available here:

  https://matthieu-moy.fr/spip/?Pre-compiled-RISC-V-GNU-toolchain-and-spike

This is known to work on Ubuntu 20.04 and 20.10. Use at your own risk anywhere
else. It contains the RiscV tools, ANTLR, and Pyright (a type-checker for Python
used in the labs).

If this works for you, perfect, you can stop here.

# Alternative 1 : docker

Docker is a lightweight alternative to virtual machines. An image with
RISC-V tools, LaTeX and Python is given here:

  https://cloud.docker.com/u/mmoy/repository/docker/mmoy/riscv-latex-python

To launch it with the current directory mounted, run:

```
sudo docker run --rm -ti -v $PWD:/home/compil --user $(id -u):$(id -g) -w /home/compil mmoy/riscv-latex-python:dev
```

The current directory on your host machine is mounted in /home/compil,
which is the default working directory. Anything access to files you
perform in this directory will actually be performed on the host
machine. Anything you do outside this directory will be lost when you
exit the docker. A typical use is to run your text editor on the host
machine, and run compilation & tests within Docker.

# Alternative 2: Installation from source (long, needs >15Gb of disk, usually requires manual hacks to get compilable stuff)

## Decide where to build and install, create directory

	# Also add the following two lines to ~/.bashrc
	export RISCV=/opt/riscv 	# Adapt as needed
	PATH="$RISCV"/bin:"$PATH"

	RISCV_BUILD="$HOME"/riscv-build # Adapt as needed

	sudo mkdir "$RISCV"
	sudo chown "$LOGNAME": "$RISCV"
	mkdir "$RISCV_BUILD"

## RISC-V C and C++ cross-compiler

	sudo apt-get install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
	## [Mac OS X] See instructions at https://github.com/riscv/riscv-gnu-toolchain#prerequisites

	cd "$RISCV_BUILD"
	git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
	cd riscv-gnu-toolchain
	./configure --prefix="$RISCV"
	make -j 4
	##[Mac OS X] only do instead of make -j 4:
	make

Quick check:

	riscv64-unknown-elf-gcc --version

Must output (version number might be more recent):

	riscv64-unknown-elf-gcc (GCC) 8.3.0
	Copyright (C) 2018 Free Software Foundation, Inc.
	This is free software; see the source for copying conditions.  There is NO
	warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Simu (spike) in riscv-tools

	sudo apt-get install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev libusb-1.0-0-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev device-tree-compiler pkg-config libexpat-dev

	## [Mac OS X] See instructions at https://github.com/riscv/riscv-tools#quickstart
	cd "$RISCV_BUILD"
	git clone --recursive https://github.com/riscv/riscv-tools.git
	cd riscv-tools/
	./build.sh
	##[Mac OS X] Edit the Makefile.in in risc-isa-sim/ and replace:
	##         $(AR) -rcs -o $$@ $$^
	## by      $(AR) rcs  $$@ $$^

Quick test:

	spike pk

Must output:

	bbl loader
	tell me what ELF to load!

## Global test (compiler + spike simulator):

    echo '#include <stdio.h>' > foo.c; printf 'int main() {printf("Hello");}' >> foo.c; riscv64-unknown-elf-gcc foo.c -o foo; spike pk ./foo; echo

Must output:

    bbl loader
    Hello

## Pyright (Python typechecker)

You need to have a recent version of nodejs and npm installed (`apt install npm` on Ubuntu 21.04, but the one provided with 20.04 is too old, otherwise install the tarball from https://nodejs.org/en/). Then, just type:

    sudo npm install -g pyright
