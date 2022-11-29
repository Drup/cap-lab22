PACKAGE = MiniC
# Example: stop at the first failed test:
#   make PYTEST_OPTS=-x tests
PYTEST_OPTS = 
# Run the whole test infrastructure for a subset of test files e.g.
#   make TEST_FILES='TP03/**/bad*.c' tests
ifdef TEST_FILES
export TEST_FILES
endif

PYTEST_BASE_OPTS=-vv -rs --failed-first --cov="$(PWD)" --cov-report=term --cov-report=html

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

all: antlr

.PHONY: antlr
antlr MiniCLexer.py MiniCParser.py: $(PACKAGE).g4
	$(ANTLR4) $< -Dlanguage=Python3 -visitor

main-deps: MiniCLexer.py MiniCParser.py MiniCTypingVisitor.py MiniCPPListener.py

%.o: %.c $(HEADERS)
	gcc -g -c -Wall -Wextra $< -o $@

$(TESTFILE:%.c=%.o): $(TESTFILE:%.c=%.cfut) $(HEADERS)
	gcc -g -c -Iinclude -Wall -Wextra -x c $(TESTFILE:%.c=%.cfut) -o $(TESTFILE:%.c=%.o)

$(TESTFILE:%.c=%.out): $(TESTFILE:%.c=%.o) lib/futurelib.o
	gcc -g $(TESTFILE:%.c=%.o) lib/futurelib.o -o $(TESTFILE:%.c=%.out) -lpthread 

$(TESTFILE:%.c=%.cfut): main-deps
	python3 MiniCC.py $(TESTFILE)

run: $(TESTFILE:%.c=%.out)
	$(TESTFILE:%.c=%.out)

test: test_futures.py main-deps
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_futures.py

tar: clean
	dir=$$(basename "$$PWD") && cd .. && \
	tar cvfz "$$dir.tgz" --exclude="*.riscv" --exclude=".git" --exclude=".pytest_cache"  \
	--exclude="htmlcov" "$$dir"
	@echo "Created ../$$(basename "$$PWD").tgz"

clean-tests:
	cd tests && \
	find . \( -iname "*.cfut" -or -iname "*.out" \) -print0 | xargs -0 rm -rf \;

clean: clean-tests
	find . \( -iname "*~" -or -iname ".cache*" -or -iname "*.diff" -or -iname "log*.txt" -or -iname "__pycache__" -or -iname "*.tokens" -or -iname "*.interp" -or -iname "*.o" \) -print0 | xargs -0 rm -rf \;
	rm -rf *~ $(PACKAGE)Parser.py $(PACKAGE)Lexer.py $(PACKAGE)Visitor.py $(PACKAGE)Listener.py .coverage .benchmarks
