#include "printlib.h"

int main() {
    string s;
	println_string(s);
    s = s + "Coucou";
    println_string(s);
	return 0;
}

// EXPECTED
// 
// Coucou