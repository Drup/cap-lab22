#include "printlib.h"

int f(int x, bool y);

int f(int x, bool y){
  return 2;
}

int f(int x, bool y){
    return 0;
}

int main(){
  bool b;
  b = f(12);
  return 0;
}


// EXITCODE 2
// EXPECTED
// In function f: Line 9 col 0: function f already defined

