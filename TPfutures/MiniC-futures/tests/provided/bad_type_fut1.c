#include "compat.h"

// Call future
int slow(int x)
{
    int i;
    i=0;
    while (i<1000) { i=i+1 ; x=2*i+x;}
    return x;
}

int summ(int x)
{
    int ret,i;
    if (x == 1)
        ret=1;
    else
    {
        ret = x + summ(x - 1);
        i=0;
        while (i<100) { i=i+1 ; x=slow(2);}
    }
    return ret;
}
int main()
{
    int val;
    
    val=Async(summ,1);
    println_int(val);

    return 0;
}

// EXITCODE 2
// EXPECTED
// In function main: Line 29 col 4: type mismatch for val: integer and futinteger

