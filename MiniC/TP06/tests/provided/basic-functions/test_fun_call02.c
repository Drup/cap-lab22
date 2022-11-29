#include "printlib.h"

// Call of function with a single parameter

int f(int x){
  int y ;
  y = 42;
  return y;
}

int main(){
  int val;
  val = f(12);
  println_int(val);
  return 0;
}

// EXPECTED
// 42
