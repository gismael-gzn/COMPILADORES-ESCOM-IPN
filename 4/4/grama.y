%{
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
%}

%union
{
	double floating; 
}

%token <floating> FPNUM
%type <floating> fexpr

%left '+'
%left '-'
%left '*'
%left '/'
%left 'E'

%%

input: /*  */ | input line;

line: '\n' | fexpr '\n' {printf("bison, resultado %lf\n", $1);}
;

fexpr: FPNUM {$$ = $1;} | fexpr '+' fexpr {$$ = $1+$3;} | fexpr '*' fexpr {$$ = $1*$3;}
		| fexpr '/' fexpr {$$ = $1/$3;} | fexpr 'E' fexpr {$$ = pow($1, $3);}
;

%%

int main() 
{
	yyparse();
}

yyerror(char *s)
{
	printf("ADVERTENCIA %s", s);
}

int yywrap()
{
	return 1;
}



