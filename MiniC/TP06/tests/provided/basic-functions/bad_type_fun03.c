#include "printlib.h"

int f(int x){
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
// In function main: Line 11 col 2: type mismatch for b: boolean and integer

