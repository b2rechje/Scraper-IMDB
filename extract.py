# Name: Brechje Seegers
# Student number: 13312960
"""
Program extract that reads data from a csv-file and generates a
dataframe from it. It returns a outputcsv-file with the top5 movies
of each year, sorted by rating.
"""

import pandas as pd
import argparse


def main(top_n, input_file_name, output_file_name):
    # Read de dataframe from csv
    df = pd.read_csv(input_file_name)
    
    n = top_n

    # Sort movies
    df = df.sort_values(by=["year", "rating"], ascending=False)

    # Filter data frame so that the top N films of each year contain
    df = df.groupby("year").head(n)

    # Read DataFrame to csv
    df.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    # Set up parsing command line arguments
    parser = argparse.ArgumentParser(description="extract top N movies")

    # Adding arguments
    parser.add_argument("-n", "--top_N", type=int, default=5, help="Top N movies (default: 5")
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("output", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.top_N, args.input, args.output)




