#include "printlib.h"

int main() {
    
    int a,n;
    
    n = 1;
    a = 7;
    while (n < a) {
      n = n+1;
    }
    println_int(n);
    
    return 0;
}

// EXPECTED
// 7
