#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

// PROTOTYPE functions
bool valid_key(string key);
string encrypt_message(string key, string text);

int main(int argc, string argv[])
{
    // if the user dont type one argument, return 1 and error message
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // if user type a argument (key), call the function and return true or false
    // if the key is valid
    bool key = valid_key(argv[1]);

    // if key is not valid, return 1 and error message
    if (key == false)
    {
        printf("Invalid key!\n");
        return 1;
    }

    // get input from user
    string text = get_string("plaintext: ");

    // call function for encrypt text
    string ciphertext = encrypt_message(argv[1], text);

    // print text encrypt and return 0
    printf("ciphertext: %s", ciphertext);

    printf("\n");

    return 0;
}

// function for validate key
bool valid_key(string key)
{
    int num_valid_characters = 0;
    int length_key = strlen(key);
    char compare_char;
    bool is_valid = true;

    for (int i = 0; i < length_key; i++)
    {
        if (isalpha(key[i]))
        {
            // if each character is alphabetical, sum 1 to num_valid_characteres
            num_valid_characters++;

            // in this if, I compare each character with the next, if are equals is_valid = false
            if (compare_char != tolower(key[i]))
            {
                compare_char = tolower(key[i]);
            }
            else
            {
                is_valid = false;
            }
        }
        else
        {
            is_valid = false;
        }
    }

    // if the key have 26 characters and is valid, return true, else return false
    if (num_valid_characters != 26 || is_valid == false)
    {
        return false;
    }
    else
    {
        return true;
    }
}

string encrypt_message(string key, string text)
{
    int n = strlen(text);

    for (int i = 0; i < n; i++)
    {
        if (isupper(text[i]))
        {
            text[i] = toupper(key[text[i] - 'A']);
        }
        else if (islower(text[i]))
        {
            text[i] = tolower(key[text[i] - 'a']);
        }
        else
        {
            text[i] = text[i];
        }
    }

    return text;
}