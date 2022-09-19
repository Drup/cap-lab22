grammar Arit;

// MIF08@Lyon1 and CAP@ENSL, arit evaluator

@header {
# header - mettre les déclarations globales
import sys
idTab = {};

class UnknownIdentifier(Exception):
    pass

class DivByZero(Exception):
    pass

}

prog: ID {print("prog = "+str($ID.text));} ;


COMMENT
 : '//' ~[\r\n]* -> skip
 ;

ID : ('a'..'z'|'A'..'Z')+;
INT: '0'..'9'+;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
