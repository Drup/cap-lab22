#include "printlib.h"

int main(){
  println_int(true+true);
  return 0;
}
// EXITCODE 2
// EXPECTED
// In function main: Line 4 col 14: invalid type for additive operands: boolean and boolean
