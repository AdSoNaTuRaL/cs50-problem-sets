#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Heigh: ");
    }
    while (height > 8 || height < 1);

    // logic first pyramid
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            // if i + j is greater or equals to height - 1 so print hash, otherwise print space
            if ((i + j) >= height - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }

        // spaces between pyarmid
        printf("  ");


        // second pyramid without space logic
        for (int k = 0; k < height; k++)
        {
            if ((k == i) || (i > k))
            {
                printf("#");
            }
        }
        printf("\n");
    }
}