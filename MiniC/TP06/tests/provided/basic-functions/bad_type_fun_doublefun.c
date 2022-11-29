#include "printlib.h"

int f(int x, bool y);

int f(int x, int y){
  int y ;
  y = 42;
  return y;
}


int main(){
  bool b;
  b = f(12);
  return 0;
}


// EXITCODE 2
// EXPECTED
// In function f: Line 5 col 0: function f already declared with a different signature
