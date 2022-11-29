#include "printlib.h"

int f(int x){
  int y ;
  y = 42;
  return y;
}

int main(){
  int x ;
  x = f(41, 41);
  println_int(x);
  return 0;
}


// EXITCODE 2
// EXPECTED
// In function main: Line 11 col 6: wrong number of arguments in call to function f
