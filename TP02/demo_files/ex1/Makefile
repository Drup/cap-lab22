MAINFILE = main
PACKAGE = Example1

ifndef ANTLR4
$(error variable ANTLR4 is not set)
endif

default: $(PACKAGE).py

$(PACKAGE).py: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3

run: $(MAINFILE).py $(PACKAGE)*.py
	python3 $<

clean:
	rm -rf *~ $(PACKAGE)*.py $(PACKAGE)*.pyc *.interp *.tokens  __pycache*
