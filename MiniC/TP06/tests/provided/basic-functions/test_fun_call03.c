#include "printlib.h"

// Call of function with two parameters

int f(int x, int y){
  return x + y;
}

int main(){
  int val;
  val = f(12, 30);
  println_int(val);
  return 0;
}

// EXPECTED
// 42
