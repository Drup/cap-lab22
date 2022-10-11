#include "printlib.h"

int main()
{
    int n, u, v;
    n = 6;
    u = 0;
    while (n > 1)
    {
        n = n - 1;
        u = u + n;
    }
    println_int(u);
    return 0;
}

// EXPECTED
// 15