#include "stdio.h"

typedef char * string;
typedef int bool;
static const int true = 1;
static const int false = 0;

void print_int(int i) {printf("%i",i);}
void println_int(int i) {printf("%i\n",i);}

void print_string(string);
void println_string(string);
