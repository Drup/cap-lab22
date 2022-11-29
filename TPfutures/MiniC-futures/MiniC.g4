grammar MiniC;

prog: include* function* EOF #progRule;

//include statements reduced to string
include: INCLUDE STRING #includestat ;

function
    : typee ID OPAR param_l? CPAR OBRACE vardecl_l block RETURN expr SCOL CBRACE  #funcDef
    | typee ID OPAR param_l? CPAR SCOL  #funcDecl
    ;

vardecl_l: vardecl* #varDeclList;

vardecl: typee id_l SCOL #varDecl;

param: typee ID  #paramDecl;

param_l
    : param              #paramListBase
    | param COM param_l  #paramList
    ;

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

if_stat: IF OPAR expr CPAR then_block=stat_block (ELSE else_block=stat_block)? #ifStat;

stat_block
    : OBRACE block CBRACE
    | stat
    ;

while_stat: WHILE OPAR expr CPAR body=stat_block #whileStat;


print_stat
    : PRINTINT OPAR expr CPAR SCOL         #printlnintStat
    | PRINTFLOAT OPAR expr CPAR SCOL       #printlnfloatStat
    | PRINTBOOL OPAR expr CPAR SCOL        #printlnboolStat
    | PRINTSTRING OPAR expr CPAR SCOL      #printstringStat
    ;

expr_l
    : expr              #exprListBase
    | expr COM expr_l   #exprList
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
    | ID OPAR expr_l? CPAR                  #funcCall
    | GET OPAR expr CPAR                   #getCall
    | ASYNC OPAR ID COM expr_l? CPAR       #asyncFuncCall
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
    : mytype=(INTTYPE|FLOATTYPE|BOOLTYPE|STRINGTYPE|FUTINTTYPE) #basicType
    ;


ASYNC : 'Async';
GET : 'Get';
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
PRINTINT : 'println_int';
PRINTBOOL : 'println_bool';
PRINTSTRING : 'println_string';
PRINTFLOAT : 'println_float';

FUTINTTYPE: 'futint';
INTTYPE: 'int';
FLOATTYPE: 'float';
STRINGTYPE: 'string';
BOOLTYPE : 'bool';
INCLUDE : '#include';

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
// BUT now we want to keep includes => # removed
 :  '//' ~[\r\n]* -> skip
 ;

SPACE
// here is a little for code rewriting.
 : [ \t\r\n] ->  channel(HIDDEN)
 ;

