ID [a-zA-Z_]+[_a-zA-Z0-9]*

BINOP [\+\-\*%/]|\*{2}

INTEGER [\+|\-]?[0-9]+

FLOATING [\+|\-]?[0-9]+"\."{1}[0-9]+

OP ([\+|\-]?{ID}|{INTEGER}|{FLOATING}){BINOP}([\+|\-]?{ID}|{INTEGER}|{FLOATING})

%%
{INTEGER} { printf("Entero"); }

{FLOATING} { printf("Flotante"); }

{ID} { printf("Identificador"); }

{OP} { printf("Operacion binaria"); }
