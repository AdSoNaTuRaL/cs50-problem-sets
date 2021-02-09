from cs50 import get_int

# get height from user - if input is less than 1 and  or more than 8, repeat
while True:
    height = get_int("Height (between 1 and 8): ")
    if height in range(1, 9):
        break

# print first pyramid
for i in range(0, height):
    for j in range(0, height):
        if ((i + j) >= height - 1):
            print("#", end="")
        else:
            print(" ", end="")

    # print space between the pyramids
    print("  ", end="")

    # print the second pyramid
    for k in range(0, height):
        if ((k == i) or (i > k)):
            print("#", end="")
    print("")

