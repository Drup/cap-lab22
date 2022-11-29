#include "printlib.h"

int f(int x){
  int y ;
  y = 42;
  return y;
}

int main(){
  int x ;
  bool b;
  b = true;
  x = f(b);
  println_int(x);
  return 0;
}

// EXITCODE 2
// EXPECTED
// In function main: Line 13 col 6: type mismatch for method argument in call to function f: boolean and integer
