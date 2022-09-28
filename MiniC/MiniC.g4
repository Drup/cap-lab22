grammar MiniC;

prog: function* EOF #progRule;

// For now, we don't have "real" functions, just the main() function
// that is the main program, with a hardcoded profile and final
// 'return 0'.
function: INTTYPE ID OPAR CPAR OBRACE vardecl_l block
	RETURN INT SCOL CBRACE #funcDef;

vardecl_l: vardecl* #varDeclList;

vardecl: typee id_l SCOL #varDecl;


id_l
    : ID              #idListBase
    | ID COM id_l     #idList
    ;

block: stat*   #statList;

stat
    : assignment SCOL
    | if_stat
    | while_stat
    | print_stat  
    ;

assignment: ID ASSIGN expr #assignStat;

if_stat: IF OPAR expr CPAR then_block=stat_block
        (ELSE else_block=stat_block)? #ifStat;

stat_block
    : OBRACE block CBRACE
    | stat
    ;

while_stat: WHILE OPAR expr CPAR body=stat_block #whileStat;


print_stat
    : PRINTLN_INT OPAR expr CPAR SCOL         #printlnintStat
    | PRINTLN_FLOAT OPAR expr CPAR SCOL       #printlnfloatStat
    | PRINTLN_BOOL OPAR expr CPAR SCOL        #printlnboolStat
    | PRINTLN_STRING OPAR expr CPAR SCOL      #printlnstringStat
    ;

expr
    : MINUS expr                           #unaryMinusExpr
    | NOT expr                             #notExpr
    | expr myop=(MULT|DIV|MOD)  expr       #multiplicativeExpr
    | expr myop=(PLUS|MINUS) expr          #additiveExpr
    | expr myop=(GT|LT|GTEQ|LTEQ)  expr    #relationalExpr
    | expr myop=(EQ|NEQ) expr              #equalityExpr
    | expr AND expr                        #andExpr
    | expr OR expr                         #orExpr
    | atom                                 #atomExpr
    ;

atom
    : OPAR expr CPAR #parExpr
    | INT            #intAtom
    | FLOAT          #floatAtom
    | (TRUE | FALSE) #booleanAtom
    | ID             #idAtom
    | STRING         #stringAtom
    ;

typee
    : mytype=(INTTYPE|FLOATTYPE|BOOLTYPE|STRINGTYPE) #basicType
    ;

OR : '||';
AND : '&&';
EQ : '==';
NEQ : '!=';
GT : '>';
LT : '<';
GTEQ : '>=';
LTEQ : '<=';
PLUS : '+';
MINUS : '-';
MULT : '*';
DIV : '/';
MOD : '%';
NOT : '!';

COL: ':';
SCOL : ';';
COM : ',';
ASSIGN : '=';
OPAR : '(';
CPAR : ')';
OBRACE : '{';
CBRACE : '}';

TRUE : 'true';
FALSE : 'false';
IF : 'if';
ELSE : 'else';
WHILE : 'while';
RETURN : 'return';
PRINTLN_INT : 'println_int';
PRINTLN_BOOL : 'println_bool';
PRINTLN_STRING : 'println_string';
PRINTLN_FLOAT : 'println_float';

INTTYPE: 'int';
FLOATTYPE: 'float';
STRINGTYPE: 'string';
BOOLTYPE : 'bool';

ID
 : [a-zA-Z_] [a-zA-Z_0-9]*
 ;

INT
 : [0-9]+
 ;

FLOAT
 : [0-9]+ '.' [0-9]* 
 | '.' [0-9]+
 ;

STRING
 : '"' (~["\r\n] | '""')* '"'
 ;


COMMENT
// # is a comment in Mini-C, and used for #include in real C so that we ignore #include statements
 : ('#' | '//') ~[\r\n]* -> skip
 ;

SPACE
 : [ \t\r\n] -> skip
 ;

