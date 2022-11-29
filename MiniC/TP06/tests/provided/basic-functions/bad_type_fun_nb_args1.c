#include "printlib.h"

bool bbb(bool b0, bool b1, bool b2, bool b3, bool b4, bool b5, bool b6, bool b7, bool b8, bool b9, bool b10);

bool bbb(bool b0, bool b1, bool b2, bool b3, bool b4, bool b5, bool b6, bool b7, bool b8, bool b9, bool b10){
   return b9;
}

bool main() {
	bool dummy;
	dummy = bbb(true, true, true, true, true, true, true, true, true, false);
	return dummy;
}

// EXITCODE 2
// EXPECTED
// In function bbb: Line 3 col 0: function bbb declared with 11 > 8 arguments
