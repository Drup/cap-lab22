grammar Tree;


int_tree_top : int_tree EOF #top
    ;

int_tree:  INT    #leaf
    | '(' INT int_tree+ ')'  #node
    ;


INT: [0-9]+;
WS  :   (' '|'\t'|'\n')+  -> skip;



