#include "printlib.h"

int main() {
    bool x;
    if (x) {
        println_int(1);
    }
    x = !x;
    if (x) {
        println_int(2);
    }
    return 0;
}

// EXPECTED
// 2
