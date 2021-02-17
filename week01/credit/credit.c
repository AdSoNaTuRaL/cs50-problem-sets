#include <stdio.h>
#include <cs50.h>
#include <unistd.h>

int main(void)
{
    long card_number = get_long("Enter with your credit card number: ");

    int last_digit, total, last_two_digits;
    int checksum = 0;
    int anothers_digits = 0;
    int i = 1;

    do
    {
        // Here I get the last digit (by getting mod of card_number/10) each time pass in the loop
        last_digit = card_number % 10;
        // Here I get the rest of card_number each time pass in loop
        card_number = card_number / 10;

        // this if only get the two digits of card_number (i.e. => 435201059 => 43)
        if (card_number < 100 && card_number > 9)
        {
            last_two_digits = card_number;
        }

        // Here I get the digits, in the card_number,
        if (i % 2 != 0)
        {
            anothers_digits += last_digit;
            total = checksum + anothers_digits;
        }
        else
        {
            // this verify if the digits are greater than 5, cause if so, I have to sum them (i.e. 6 * 2 = 12 => (1 + 2 =3))
            if (last_digit >= 5)
            {
                checksum = checksum + (last_digit * 2) / 10;
                checksum = checksum + (last_digit * 2) % 10;
            }
            else
            {
                checksum = checksum + (last_digit * 2);
            }



            total = checksum + anothers_digits;
        }

        i++;
    }
    while (card_number != 0);


    // outside the loop, I verify if total (checksum + others_digits) last digit`s == 0
    if (total % 10 == 0)
    {
        // then I verify if lenght of digits and if last two digits fits in some card category
        if (((i - 1) == 15) && (last_two_digits == 34 || last_two_digits == 37))
        {
            printf("AMEX\n");
        }
        else if (((i - 1) == 16) && (last_two_digits == 51 || last_two_digits == 52 || last_two_digits == 53 ||
                                     last_two_digits == 54 || last_two_digits == 55))
        {
            printf("MASTERCARD\n");
        }
        else if (((i - 1) == 13) || ((i - 1) == 16 && last_digit == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}