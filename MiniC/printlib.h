/**
 * Compatibility layer with C (meant to be #included in MiniC source
 * files). Defines types, constants and functions that are built-in
 * MiniC, to allow compiling MiniC programs with GCC.
 */

typedef char * string;
typedef int bool;
static const int true = 1;
static const int false = 0;

void print_int(int);
void println_int(int);
void println_bool(int);

void print_float(float);
void println_float(float);

void print_string(string);
void println_string(string);
