#include "compat.h"

// Call future

int functi(int x){
  int y;
  y=x;
  y = 42;
  return y;
}

int main(){
  futint fval;
  int val;
  fval = Async(functi,123);
  val = Get(fval);
  println_int(val);
  return 0;
}

// EXPECTED
// 42
