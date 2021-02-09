#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .jpg header
const int HEADER_SIZE = 512;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open file
    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open the file\n");
        return 1;
    }

    // Create a buffer
    uint8_t buffer[HEADER_SIZE];

    // Count images
    int count_image = 0;

    int already_found = 0;

    // Create a output file
    FILE *output = NULL;

    while (fread(buffer, HEADER_SIZE, 1, input) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (already_found == 1)
            {
                fclose(output);
            }
            else
            {
                already_found = 1;
            }

            char filename[8];
            sprintf(filename, "%03i.jpg", count_image);
            output = fopen(filename,  "w");
            count_image++;
        }

        if (already_found == 1)
        {
            fwrite(&buffer, HEADER_SIZE, 1, output);
        }
    }


    fclose(output);
    fclose(input);

    return 0;

}