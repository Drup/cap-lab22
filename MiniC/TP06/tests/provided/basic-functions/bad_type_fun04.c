#include "printlib.h"

int f(int x, bool b, int z);

int main(){
  bool b;
  b = f(12,1,2);
  return 0;
}

int f(int x, bool b, int z){
    int y ;
    y = 42;
    return y;
}

// EXITCODE 2
// EXPECTED
// In function main: Line 7 col 6: type mismatch for method argument in call to function f: integer and boolean
