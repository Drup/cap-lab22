#include "printlib.h"

bool f(int x, bool b){
  int x ;
  x = 42;
  return b;
}

int main(){
  int x ;
  x = f(41, 41);
  println_int(x);
  return 0;
}

// EXITCODE 2
// EXPECTED
// In function f: Line 4 col 2: Variable x already declared

