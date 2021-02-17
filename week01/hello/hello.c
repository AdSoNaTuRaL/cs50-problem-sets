#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //get name of user
    string name = get_string("What`s your name?\n");

    printf("Hello, %s\n", name);
}