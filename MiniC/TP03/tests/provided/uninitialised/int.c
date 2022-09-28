#include "printlib.h"

int main() {
    int x;
	println_int(x);
    x = x + 1;
    println_int(x);
	return 0;
}

// EXPECTED
// 0
// 1