# Name: Brechje Seegers
# Student number: 13312960
"""
Program that visualizes the data from IMDB in a graph.
Provides a bar plot in a csv file with the actors that appear most often
"""

import pandas as pd
import argparse
import matplotlib.pyplot as plt


def main(input_file_name, output_file_name):
    # Read the input to DataFrame
    df = pd.read_csv(input_file_name)

    # Split values in column actors by semicolumn
    df['actors'] = df['actors'].str.split(';')

    # Explode column by actors
    exploded_actors = df.explode('actors')

    # Group actors by title and count them
    actors_count = exploded_actors.groupby('actors')['title'].count()

    # Sort values actors and display first 50
    top50 = actors_count.sort_values(ascending=False).head(50)

    # Make list of both columns for the bar plot
    list_actor = top50.index.tolist()
    list_count = top50.values.tolist()

    my_color = ['purple', 'orange', 'blue']

    # Make bar plot
    plt.bar(list_actor, list_count, color=my_color)
    plt.title('Top 50 actors with most appearance')
    plt.xlabel('Actors', fontsize=9)
    plt.ylabel('Number of Appearance', fontsize=9)
    plt.subplots_adjust(bottom=0.4)
    plt.xticks(list_actor, rotation='vertical')
    plt.tick_params(axis='x', labelsize=6)
    plt.grid(color='grey', linestyle='-', axis='y', alpha=0.7)
    plt.savefig('actors.png')
    plt.show()


if __name__ == "__main__":
    # Set up parsing command line arguments
    parser = argparse.ArgumentParser(description="Visualize the 50 actors with most appearance")

    # Adding arguments
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("output", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)
