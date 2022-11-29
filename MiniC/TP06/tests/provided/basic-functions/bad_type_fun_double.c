#include "printlib.h"

int f(int x, bool x){
  int y ;
  y = 42;
  return y;
}

int main(){
  int x ;
  x = f(41, 41);
  println_int(x);
  return 0;
}

// EXITCODE 2
// EXPECTED
// In function f: Line 3 col 13: Parameter x already defined

