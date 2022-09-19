//define a lexical analyser called Example1

lexer grammar Example1;

OP : '+'| '*' | '-' | '/' ;
DIGIT : [0-9] ;
LETTER : [A-Za-z] ;
ID : LETTER (LETTER | DIGIT)* ;             // match idents
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
