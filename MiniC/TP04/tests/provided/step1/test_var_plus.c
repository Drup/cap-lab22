#include "printlib.h"

int main() {
    
    int x;
    x = 42;
    println_int(x + x);
    println_int(x + 1);
    println_int(1 + x);
    return 0;
}

// EXPECTED
// 84
// 43
// 43
