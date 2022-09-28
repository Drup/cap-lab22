#include "printlib.h"

int main() {
    float x;
	println_float(x);
    x = x + 1.0;
    println_float(x);
	return 0;
}

// EXPECTED
// 0.00
// 1.00