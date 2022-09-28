grammar Arit;

prog: statement+ EOF            #statementList
    ;

statement
    : expr SCOL                 #exprInstr
    | 'set' ID '=' expr SCOL    #assignInstr
    ;

expr: expr multop=(MULT | DIV) expr     #multiplicationExpr
    | expr addop=(PLUS | MINUS) expr   #additiveExpr
    | atom                            #atomExpr
    ;

atom: INT                       #numberAtom
    | ID                        #idAtom
    | '(' expr ')'              #parens
    ;


SCOL :      ';';
PLUS :      '+';
MINUS :     '-';
MULT :      '*';
DIV :       '/';
ID:         [a-zA-Z_] [a-zA-Z_0-9]*;

INT:        [0-9]+;

COMMENT:    '#' ~[\r\n]* -> skip;
NEWLINE:    '\r'? '\n' -> skip;
WS  :       (' '|'\t')+  -> skip;
