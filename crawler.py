# Name: Brechje Seegers
# Student number: 13312960
"""
Takes from csv file all URLs of IMDB page. Reads languages per page and generates a
dataframe with how many times a language occurs in decades from 1930. Generates a png-file
with a line graph with the 10 most common languages.
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import pandas as pd


def main(input_file_name, output_file_name):
    # Read de dataframe from csv-file
    df = pd.read_csv(input_file_name)

    # List to safe all languages used
    list_df_languages = []

    # Iterate over every url in the column
    for item in df['url']:
        # Load website using the url from column
        IMDB_URL = item
        html = simple_get(IMDB_URL)
        dom = BeautifulSoup(html, 'html.parser')
        main_html = dom.find("main")

        # Get from the page the langues per film and returns a list of languages per film
        languages_list = get_languages(main_html)

        # Add list of languages by movie to the big list for all movies
        list_df_languages.append(languages_list)

    # Add the list with all languages to the already existing dataframe as a new kolo
    df.insert(4, 'languages', list_df_languages)

    # Sort dataframe by year ascending
    df = df.sort_values(by=["year"], ascending=True)

    # Convert df to csv-file
    df.to_csv(output_file_name, index=False)


"""
Function that retrieves the language or languages from 1 page.
It returns a string with every languages seperated by semicolon
It puts this in 1 string and returns
"""
def get_languages(main_html):
    
    # Find mothertag of languages
    language = main_html.find('li', attrs={"data-testid": "title-details-languages"})

    # Find child tag. This type list, iterate trough the list and extract the text.
    try:
        list_language = language.find_all('a')
    except:
        list_language = []
        
    # String of langueages per item
    new_language = ""

    # Check if there are multiple films, make them into a string and separate by ;
    for item in list_language:
        taal = item.get_text()
        new_language += taal
        new_language += ';'

    # Take off last semicolon from string
    new_language = new_language[:-1]

    # Returns string of languages for 1 movie
    return new_language


if __name__ == "__main__":
    # Set up parsing command line arguments
    parser = argparse.ArgumentParser(description="crawls languages information from URLS")

    # Adding arguments
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("output", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)
