#include "printlib.h"

int main(){
  println_int(3/2+45*(2/1));
  println_int(23+19);
  println_bool( (false || 3 != 77 ) && (42<=1515) );
  println_string("coucou");
  return 0;
}
  
// EXPECTED
// 91
// 42
// 1
// coucou
