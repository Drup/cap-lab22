#include "printlib.h"

int main() {
    int i, j;
    i = 1;
    j = i;
    println_int(j);
    return 0;
}

// EXPECTED
// 1
