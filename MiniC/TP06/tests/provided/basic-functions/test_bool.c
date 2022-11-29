#include "printlib.h"

bool bbb(bool b){
   return b;
}

int main() {
	bool dummy;
	dummy = bbb(false);
	return 0;
}

// EXPECTED
