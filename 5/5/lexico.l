%{
#include "grama.tab.h"
%}

FPNUM [0-9]+"\."{1}[0-9]+

%%

{FPNUM}  {
	char *guard = NULL;
	printf("Constante entera %s\n", yytext);
	yylval.floating = strtod(yytext, &guard);
	return (FPNUM);
}

"+" {
	printf("OP suma\n");
	return *yytext;
}

"-" {
	printf("OP subs\n");
	return *yytext;
}

"*" {
	printf("OP prod\n");
	return *yytext;
}

"/" {
	printf("OP div\n");
	return *yytext;
}

"E" {
	printf("OP exp\n");
	return *yytext;
}

"\n" {
	printf("Nueva linea\n");
	return *yytext;
}

%%
