#include "printlib.h"

int main() {
    
    int n;
    
    n = 9;
    while (n > 0) {
    n = n-1 ;
    println_int(n) ;
    }
    
    return 0;
}

// EXPECTED
// 8
// 7
// 6
// 5
// 4
// 3
// 2
// 1
// 0
