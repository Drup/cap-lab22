#include "printlib.h"

int main() {
    
    int x, y;
    x = 42;
    y = 66;
    println_int(x + y);
    x = 1;
    println_int(x + y);
    y = 2;
    println_int(x + y);
    return 0;
}

// EXPECTED
// 108
// 67
// 3

