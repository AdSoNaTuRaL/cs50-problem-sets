from cs50 import get_string


def main():

    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    average_words = words / 100

    L = letters / average_words

    S = sentences / average_words

    indexColeman = int(round(0.0588 * L - 0.296 * S - 15.8))

    if (indexColeman >= 16):
        print("Grade 16+")
    elif (indexColeman < 1):
        print("Before Grade 1")
    else:
        print(f"Grade {indexColeman}")


def count_letters(text):
    num_letters = 0
    n = len(text)

    for i in range(n):
        if (text[i].isalpha()):
            num_letters += 1

    return num_letters


def count_words(text):
    num_words = 1
    n = len(text)

    for i in range(n):
        if(text[i].isspace()):
            num_words += 1

    return num_words


def count_sentences(text):
    num_sentences = 0
    n = len(text)

    dot = ord('.')
    exclamation = ord('!')
    interrogation = ord('?')

    for i in range(n):
        character = ord(text[i])
        if (character == dot or character == exclamation or character == interrogation):
            num_sentences += 1

    return num_sentences


if __name__ == "__main__":
    main()
