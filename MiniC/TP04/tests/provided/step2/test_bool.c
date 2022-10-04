#include "printlib.h"

int main() {
    
    bool b;
    b = false;
    println_bool(b);
    b = true;
    println_bool(b);
    println_bool(true);
    println_bool(false);
    return 0;
}

// EXPECTED
// 0
// 1
// 1
// 0
