# Name: Brechje Seegers
# Student number: 13312960
"""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

import code
from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
from math import ceil
import argparse
import csv
import numpy as np


def main(output_file_name, start_year, end_year):

    minvalue = 0
    pages = 1
    df = pd.DataFrame()
    
    while minvalue < 5:
        # Load website with BeautifulSoup
        IMDB_URL = f'https://www.imdb.com/search/title/?title_type=feature&release_date={start_year}-01-01,{end_year - 1}-12-31&num_votes=5000,&sort=user_rating,desc&start={pages}&view=advanced'
        html = simple_get(IMDB_URL)
        dom = BeautifulSoup(html, 'html.parser')

        # Extract movies from website
        movies_df = extract_movies(dom)

        df = pd.concat([movies_df, df])

        # Kijken hoeveel films er per jaar zijn in dit dataframe met count
        movies_count = df.groupby("year")['title'].count()

        # Check de minimum in colomn, als deze kleiner is dan 5 dan opnieuw pagina loaden
        minvalue = movies_count.min()

        # If there is no top 5 from each year, go to next page
        pages += 50

    # Sort the DataFrame based on year ascending
    df = df.sort_values('year')

    # Save results to output file
    df.to_csv(output_file_name, index=False)



def extract_movies(dom):
    # Create dictionary with keys and an empty list.
    movies = {"title": [], "rating": [], "year": [], "actors": [], "runtime": [], "url": []}

    # Loop over each lister-item-content containing the information by movie
    for item in dom.find_all('div', class_='lister-item-content'):

        # Save the title from the childtag & add to list in dictionary
        title = item.h3.a.text
        movies['title'].append(title)

        # Save the childtag for the year, remove () and add to list dictionary
        year = item.find('span', class_='lister-item-year text-muted unbold').text
        year = year.replace('(', '')
        year = year.replace(')', '')
        # If year has more than 1 string, take the actual year 
        year = year.split()
        if len(year) == 2:
            year = year[1]
            movies['year'].append(year)
        else:
            movies['year']. append(year[0])

        # Save the childtag for the url, add https and en add to list dictionary
        url = item.h3.a.get('href')
        x = "https://www.imdb.com/"
        url = x + url
        movies['url'].append(url)

        # Save the childtag for runtime. remove the 'min' and add to list dictionary
        runtime = item.find('span', class_='runtime').text
        runtime = runtime.split()[0]
        movies['runtime'].append(runtime)

        # Save the childtag for rating and add to list dictionary
        rating = item.div.strong.text
        movies['rating'].append(rating)

        # Using the parent tag of actors, find the paragraph. split the string to remove directors, 
        # removed characters and save actors. add it to list of dictionary
        actor = item.find('p', class_='').text
        actor = actor.strip().split("|")
        actors = []
        for x in actor:
            actors.append(x.replace('\n', ''))
        if len(actors) == 2:
            actors = actors[1].split(':')
            actors = actors[1].replace(',', ';')
            movies['actors'].append(actors)
        else:
            movies['actors'].append("")

    # Return Dataframe with dictionary movies
    df = pd.DataFrame(movies)  
    return df



if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-s", "--start_year", type=int, default = 1930, help="starting year (default: 1930)")
    parser.add_argument("-e", "--end_year",   type=int, default = 2020, help="starting year (default: 2020)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.start_year, args.end_year)
