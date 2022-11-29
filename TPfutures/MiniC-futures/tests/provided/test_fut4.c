#include "compat.h"

// Call future

int slow(int x)
{
    int i,t;
    i=0;
    t=0;
    while (i<x*1000) { i=i+1 ; t=t+2*i+x;}
    return t;
}

int summ(int x)
{
    int ret;
    int i;
    if (x == 1)
        ret=1;
    else
    {
        ret = x + summ(x - 1);
        i=0;
        while (i<100) { i=i+1 ; x=slow(20);}
    }
    return ret;
}



int summandprint(int x)
{
    int ret;
    ret=summ(x);
    println_int(ret);
    return ret;
}


int main()
{
    int val;
    futint f,g;
    
    f=Async(summandprint,500);
    g=Async(summandprint,2);
    
    val=Get(f)+Get(g);

    return 0;
}


// EXPECTED
// 3
// 125250
