#include "compat.h"

// Call future

int summ(int x)
{
    int ret;
    if (x == 1)
        ret=1;
    else
    {
        ret=x + summ(x - 1);
    }
    return ret;
}

int useFuture(futint f)
{
    int x;
    x=Get(f);
    return x+1;
}


int main()
{
    int val,x;
    futint f,g;
    
    f=Async(summ,15);
    g=Async(summ,16);
    
    val=Get(f)+Get(g)+useFuture(g);
    println_int(val);

    return 0;
}


// EXPECTED
// 393  
