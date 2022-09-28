#include "printlib.h"

int main(){
  string n,m;
  n = "foo";
  m = "bar";
  println_string(n);
  println_string(m);
  println_string(n + m);
  return 0;
}

// EXPECTED
// foo
// bar
// foobar
