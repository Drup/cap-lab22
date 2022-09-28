#include "printlib.h"

int main(){
  int n;
  n=17;
  m=n+3;
  println_int(m);
  return 0;
}
  
// EXPECTED
// EXITCODE 2
// In function main: Line 6 col 2: Undefined variable m
