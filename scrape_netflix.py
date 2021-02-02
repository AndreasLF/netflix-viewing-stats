from googlesearch import search
import pandas as pd
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup


def get_english_title(title):
    # Make a google search on netlfix.com
    query = '{} site:netflix.com'.format(title)
    result = search(query, lang="en")

    if result:
        # Take the first url
        url = result[0]

        r = re.findall("https://www.netflix.com/(.*)/title/(.*)", url)

        if not r:
            return None 

        netflix_id = r[0][1]

        url = "https://www.netflix.com/dk-en/title/{}".format(netflix_id)
        
        # Open the page and decode to html string
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        # Parse html
        soup = BeautifulSoup(html, 'html.parser')
        title_element = soup.find(attrs={"class": "title-title"})
        english_title = title_element.contents[0]
    else:
        english_title = None

    return english_title


def get_episode_runtime(title, season, episode):
    """Gets the runtime of a series episode on Netflix.

    Notice that the language is set to Danish. Netflix results will be in Danish

    Args:
        title (str): The series title.
        season (str): The season name.
        episode (str): The episode name.

    Returns:
        str: The duration of the series episode.
    """

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
    season_selector = season_selector.find_all("option")

    # Create a dictionairy with season names and their value
    season_dict = {}
    for s in season_selector:
        value = int(s.get("value"))
        season_name = s.contents[0]
        season_dict[season_name] = value

    print(season_dict)


    season_containers = soup.find_all("div", class_="season")

    episode_metadata = season_containers[season_dict[season]].find_all("div", class_="episode-metadata")

    # Loop through episodes
    for ep in episode_metadata:
        # Get title
        episode_name = ep.find(attrs={"class": "episode-title"}).contents[0]

        regex = ".*{}$".format(episode)
        if re.search(regex, episode_name):
            runtime = ep.find(attrs={"class": "episode-runtime"}).contents[0]
            return runtime


# print(get_episode_runtime("Kyle XY", "Season 2", "Time of Death"))
# print(get_english_title("En mand med tusind ansigter"))
