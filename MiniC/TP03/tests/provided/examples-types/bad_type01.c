#include "printlib.h"

int main(){
  int n;
  string s;
  n=17;
  s="seventeen";
  s = n*s;
  return 0;
}

// EXITCODE 2
// EXPECTED
// In function main: Line 8 col 6: invalid type for multiplicative operands: integer and string
