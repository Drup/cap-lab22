#include "printlib.h"

// Definition of function with a single parameter
// with forward declaration, i.e. declaration here and definition after main
int f(int x);

int main(){
  int z;
  z = f(0);
  return 0;
}

int f(int x){
    int y ;
    y = 42;
    return y;
}


// EXPECTED
