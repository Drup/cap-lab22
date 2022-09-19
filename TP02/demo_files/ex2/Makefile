MAINFILE = main
PACKAGE = Example2

ifndef ANTLR4
$(error variable ANTLR4 is not set)
endif

default: $(PACKAGE)Parser.py

$(PACKAGE)Parser.py: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3

run: $(MAINFILE).py $(PACKAGE)Parser.py
	python3 $<

clean:
	rm -rf *~ $(PACKAGE)*.py $(PACKAGE)*.pyc *.interp *.tokens  __pycache*
