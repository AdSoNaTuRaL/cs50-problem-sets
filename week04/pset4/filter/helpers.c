#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sr = round((.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue));
            int sg = round((.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue));
            int sb = round((.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue));

            if (sr > 255)
            {
                sr = 255;
            }

            if (sg > 255)
            {
                sg = 255;
            }

            if (sb > 255)
            {
                sb = 255;
            }

            image[i][j].rgbtRed = sr;
            image[i][j].rgbtGreen = sg;
            image[i][j].rgbtBlue = sb;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int startIndex = 0;
        int endIndex = width - 1;

        while (startIndex < endIndex)
        {
            RGBTRIPLE temp = image[i][startIndex];
            image[i][startIndex] = image[i][endIndex];
            image[i][endIndex] = temp;

            startIndex++;
            endIndex--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    float r, b, g;
    float counter = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (i + k >= 0 && j + l >= 0 && i + k <= height - 1 && j + l <= width - 1)
                    {
                        r += copy[i + k][j + l].rgbtRed;
                        b += copy[i + k][j + l].rgbtBlue;
                        g += copy[i + k][j + l].rgbtGreen;
                        counter++;
                    }

                }
            }

            r = r / counter;
            b = b / counter;
            g = g / counter;

            if (r > 255)
            {
                r = 255;
            }

            if (r < 0)
            {
                r = 0;
            }

            if (g > 255)
            {
                g = 255;
            }

            if (g < 0)
            {
                g = 0;
            }

            if (b > 255)
            {
                b = 255;
            }

            if (b < 0)
            {
                b = 0;
            }

            image[i][j].rgbtRed = round(r);
            image[i][j].rgbtBlue = round(b);
            image[i][j].rgbtGreen = round(g);

            counter = 0;

            r = 0;
            g = 0;
            b = 0;
        }
    }
    return;
}
