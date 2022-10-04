#include "printlib.h"

int main() {
    
    if (10 == 10) {
    println_int(12);
    } else if (10 == 10) {
    println_int(15);
    } else {
    println_int(13);
    }
    println_int(14);
    return 0;
}

// EXPECTED
// 12
// 14

