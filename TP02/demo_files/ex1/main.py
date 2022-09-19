from antlr4 import InputStream
from antlr4 import CommonTokenStream
from Example1 import Example1

import sys


def main():
    # InputStream reads characters (from stdin in our case)
    input_stream = InputStream(sys.stdin.read())
    # The generated lexer groups characters into Tokens ...
    lexer = Example1(input_stream)
    # ... and the stream of Tokens is managed by the TokenStream.
    stream = CommonTokenStream(lexer)

    # Display the token stream
    stream.fill()  # needed to get stream.tokens (otherwise lazily filled-in)
    for t in stream.tokens:
        print(t)
    print("Finished")


# warns pb if py file is included in others
if __name__ == '__main__':
    main()
