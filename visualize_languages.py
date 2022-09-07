# Name: Brechje Seegers
# Student number: 13312960
"""
Programma dat de data uit IMDB visualiseerd in een grafiek
die de taalinvloed in de bestbeoordeeelde films laat zien van afgelopen 9 decennia
"""

import pandas as pd
import argparse
import matplotlib.pyplot as plt


def main(input_file_name, output_file_name):
    # Read the input to DataFrame
    df = pd.read_csv(input_file_name)

    # Split values in column actors by semicolumn
    df['languages'] = df['languages'].str.split(';')

    # Nieuwe kolom decades toegevoegd
    df['decade'] = 10 * (df['year'] // 10)

    # Explode column by languages -(alle talen uitgezet) Hiervan tellen hoevaak elke taal voorkomt per decade
    df = df.explode('languages')

    # Count all languages
    df = df.pivot_table('title', index='languages', columns='decade', aggfunc='count')

    # Fill missing values (NaN) with value
    df = df.fillna(0)

    # Calculate mean of each language in dataframe
    av_per_language = df.mean(axis=1)

    # Add average column to dataframe
    df['mean'] = av_per_language

    # Sort values by mean
    df = df.sort_values(by=['mean'], ascending=False).head(10)

    # Drop column with mean values
    top10 = df.drop(columns=['mean'])

    # Transposing dataframe to make list of columns
    top10 = top10.T

    # Make column of index
    top10.reset_index(inplace=True)
    top10 = top10.rename(columns={'index': 'decade'})

    # Plot lines in line chart
    plt.plot(top10['decade'], top10['English'], color='g', label='English')
    plt.plot(top10['decade'], top10['French'], color='r', label='French')
    plt.plot(top10['decade'], top10['German'], color='b', label='German')
    plt.plot(top10['decade'], top10['Italian'], color='c', label='Italian')
    plt.plot(top10['decade'], top10['Russian'], color='m', label='Russian')
    plt.plot(top10['decade'], top10['Japanese'], color='y', label='Japanese')
    plt.plot(top10['decade'], top10['Spanish'], color='b', label='Spanish')
    plt.plot(top10['decade'], top10['Turkish'], color='k', label='Turkish')
    plt.plot(top10['decade'], top10['Tamil'], color='pink', label='Tamil')
    plt.plot(top10['decade'], top10['Hindi'], color='orange', label='Hindi')

    plt.legend()
    plt.savefig('languages.png')
    plt.show()


if __name__ == "__main__":
    # Set up parsing command line arguments
    parser = argparse.ArgumentParser(description="Visualize the top 10 languages over 9 decennia")

    # Adding arguments
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("output", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)
