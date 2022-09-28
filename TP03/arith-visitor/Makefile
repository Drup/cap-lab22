PACKAGE = Arit
MAINFILE = arit

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor

run: $(MAINFILE).py
	python3 $^

ex: $(MAINFILE).py
	python3 $^ < myexample

test: all
	python3 ./test_arith_visitor.py

clean:
	find . \( -iname "~" -or -iname "*.cache*" -or -iname "*.diff" -or -iname "log.txt" -or -iname "*.pyc" -or -iname "*.tokens" -or -iname "*.interp" \) -exec rm -rf '{}' \;
	rm -rf $(PACKAGE)*.py
