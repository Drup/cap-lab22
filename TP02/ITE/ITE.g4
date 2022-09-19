grammar ITE;

prog: stmt EOF;

stmt : ifStmt | ID ;

ifStmt : 'if' ID 'then' thenstmt=stmt ('else' elsestmt=stmt)?;


ID : [a-zA-Z]+;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
