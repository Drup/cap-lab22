//define a tiny grammar with attributes for arith expressions with identifiers

grammar Example3;

full_expr: e0=expr ';' EOF {print($e0.text + " has " + str($e0.count) + " operators!")} ;

expr returns [int count]:  // expr has an integer attribute called count
    | e0=expr OP e1=expr {$count = $e0.count + $e1.count + 1}  // name sub-parts and access their attributes
    | ID {$count = 0}
    | INT {$count = 0}
    ;

OP : '+'| '*' | '-' | '/' ;


INT : '0'..'9'+ ;
ID : ('a'..'z'|'A'..'Z')+ ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
