from cs50 import get_int

card_number = get_int("Number: ")

i = 1
checksum = 0
another_digits = 0

while True:
    last_digit = card_number % 10
    card_number = int(card_number / 10)

    if (card_number < 100 and card_number > 9):
        last_two_digits = card_number

    if (i % 2 != 0):
        another_digits += last_digit
        total = checksum + another_digits
    else:
        if (last_digit >= 5):
            checksum = int(checksum + (last_digit * 2) / 10)
            checksum = checksum + (last_digit * 2) % 10
        else:
            checksum = checksum + (last_digit * 2)

        total = checksum + another_digits

    i += 1

    if (card_number == 0):
        break

if (total % 10 == 0):
    if (((i - 1) == 15) and (last_two_digits in [34, 37])):
        print("AMEX")
    elif (((i - 1) == 16) and (last_two_digits in [51, 52, 53, 54, 55])):
        print("MASTERCARD")
    elif (((i - 1) == 13) or ((i - 1) == 16 and last_digit == 4)):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")