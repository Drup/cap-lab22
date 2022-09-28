#include "printlib.h"

int main() {
    if ((1.0 + 2.0) * 3.0 == 9.0) {
        println_string("OK");
    }
    return 0;
}

// EXPECTED
// OK
