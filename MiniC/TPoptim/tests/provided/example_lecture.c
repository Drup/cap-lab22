#include "printlib.h"

int main() {
    int i, j, k;
    i = 1;
    j = 1;
    k = 0;
    while (k < 100) {
    	if (j < 20) {
	    j = i;
	    k = k+1;
    	}
    	else {
            j = k;
            k = k+2;
    	}
    }
    println_int(j);
    return 0;
}

// EXPECTED
// 1
