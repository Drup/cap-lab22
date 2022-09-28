#include "printlib.h"

int main(){
  println_int("foo");
  return 0;
}
  
// EXITCODE 2
// EXPECTED
// In function main: Line 4 col 2: invalid type for println_int statement: string

