#include "printlib.h"

int main()
{
    if (2 < 3)
    {
        println_int(1);
    }
    if (2 > 3)
    {
        println_int(2);
    }
    if (2 <= 2)
    {
        println_int(3);
    }
    if (2 >= 2)
    {
        println_int(4);
    }

    if (2 == 3)
    {
        println_int(10);
    }
    if (2 != 3)
    {
        println_int(20);
    }
    if (2 == 2)
    {
        println_int(30);
    }
    if (2 != 2)
    {
        println_int(40);
    }

    return 0;
}

// EXPECTED
// 1
// 3
// 4
// 20
// 30
