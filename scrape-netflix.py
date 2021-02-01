from googlesearch import search
import pandas as pd
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

# Series title
title = "Suits"

# Make a google search on netlfix.com
query = '{} site:netflix.com'.format(title)
result = search(query, lang="dk")

# Take the first url
url = result[0]

# Open the page and decode to html string
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Parse html
soup = BeautifulSoup(html, 'html.parser')


# Find the season selector element
season_selector = soup.find(attrs={"id": "undefined-select"})
# Find all option elements in the season selector element
seasons = season_selector.find_all("option")

# Create a dictionairy with season names and their value
season_dict = {}
for season in seasons:
    value = int(season.get("value"))
    season_name = season.contents[0]
    season_dict[season_name] = value

print(season_dict)

episode_metadata = soup.find_all("div", class_="episode-metadata")

# Loop through episodes
for episode in episode_metadata:
    # Get title and duration
    title = episode.find(attrs={"class": "episode-title"}).contents[0]
    runtime = episode.find(attrs={"class": "episode-runtime"}).contents[0]
    print(title, runtime)