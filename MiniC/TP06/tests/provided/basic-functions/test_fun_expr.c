#include "printlib.h"

int f(int x){
   return x + 1;
}

int main() {
	int dummy;
	dummy = f(f(10) + f(100));
	println_int(dummy);
	return 0;
}

// EXPECTED
// 113
