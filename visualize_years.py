
# Name: Brechje Seegers
# Student number: 13312960
"""
Program that visualizes the data from IMDB in a graph.
Provides a bar plot showing the average rating of the top 5 films per year
"""

import pandas as pd
import argparse
import matplotlib.pyplot as plt


def main(input_file_name, output_file_name):
    # Read the input to DataFrame
    df = pd.read_csv(input_file_name)

    # Make new Dataframe with average rating per year
    df = df.groupby("year")['rating'].mean().reset_index()

    # Make list of columns dataframe
    list_year = df["year"].tolist()
    list_average_rating = df["rating"].tolist()

    my_color = ['green', 'orange', 'brown', 'dodgerblue', 'red']

    # Make bar plot
    plt.bar(list_year, list_average_rating, color=my_color)
    plt.title('Average rating of top 5 film per year')
    plt.xlabel('Year')
    plt.ylabel('Average rating score')
    plt.xlim(1930, 2020)
    plt.ylim(7, 9)
    plt.grid(color='grey', linestyle='-', axis='y', alpha=0.7)
    plt.savefig('years.png')
    plt.show()


if __name__ == "__main__":
    # Set up parsing command line arguments
    parser = argparse.ArgumentParser(description="Visualize average rating of the top 5 films")

    # Adding arguments
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("output", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)
