#include "printlib.h"

int main(){
  int x;
  x="blabla";
  return 0;
}
  
// EXPECTED
// In function main: Line 5 col 2: type mismatch for x: integer and string
// EXITCODE 2
