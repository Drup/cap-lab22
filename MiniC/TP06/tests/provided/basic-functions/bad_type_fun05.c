#include "printlib.h"

int f(int x, bool b, int z);

int main(){
  int b;
  b = f(12,true,2);
  return 0;
}

int f(int x, bool b, int z){
    int y ;
    y = 42;
    return true;
}

// EXITCODE 2
// EXPECTED
// In function f: Line 11 col 0: type mismatch for return type of function f: integer and boolean
