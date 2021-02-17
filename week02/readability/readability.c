#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <string.h>

// PROTOTYPE functions count_letters, count_words and count_sentences
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // get input from the user
    string text = get_string("Text: ");

    // get number of letters, words and sentence of a text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float average_words = (float) words / 100;

    float L = (float) letters / average_words;

    float S = (float) sentences / average_words;

    // Coleman-Liau index
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Convert index for int
    int indexColeman = (int) round(index);

    if (indexColeman >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (indexColeman < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", indexColeman);
    }

}


int count_letters(string text)
{
    // variable for count num of letters
    int num_letters = 0;

    // loop inside each character of text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // if character is alphabetical, sum 1 to variable num_letters
        if (isalpha(text[i]))
        {
            num_letters++;
        }
    }

    return num_letters;
}

int count_words(string text)
{
    // variable for count num of words
    // variable starts in 1 cause need count the last word in a text (wich not contains space)
    int num_words = 1;

    // loop inside each character of text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // if character is space, sum 1 to variable num_words
        if (isspace(text[i]))
        {
            num_words++;
        }
    }

    return num_words;
}

int count_sentences(string text)
{
    // variable for count num of sentences
    int num_sentences = 0;

    // loop inside each character of text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // if character is space, sum 1 to variable num_words
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            num_sentences++;
        }
    }

    return num_sentences;
}