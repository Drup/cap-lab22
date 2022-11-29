#include "compat.h"

// Call future

int functi(int x){
  int y;
  y=x;
  y = 42;
  println_int(0);
  return y;
}

int main(){
  futint fval;
  fval = Async(functi,123);
  return 0;
}

// EXPECTED
// 0
