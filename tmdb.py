import json
from urllib.request import urlopen
from urllib.parse import quote
import re
from bs4 import BeautifulSoup

# Get API key for tmdb
def get_api_key_from_file(path):
    with open(path) as f:
        json_data = json.load(f)
        API_KEY = json_data["api"]
        f.close()
    return API_KEY

def tmdb(query):
    """Make api request 

    Notice that the language is set to Danish. Netflix results will be in Danish

    Args:
        query (str): Api query.

    Returns:
        json: Results. 
    """

    url = "https://api.themoviedb.org/3/{}".format(query)
    webURL = urlopen(url)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))

    return JSON_object

def search_movie(search_string, api_key):
    # Parse search string
    search_string = quote(search_string)
    # Create the search url
    query = "search/movie?api_key={}&query={}&page=1".format(api_key, search_string)
    result = tmdb(query)
    
    if result["results"]:
        movie_id = result["results"][0]["id"]

        query = "movie/{}?api_key={}".format(movie_id, api_key)
        result = tmdb(query)
    else:
        return None

    return result

def get_episode(search_string, season_number, episode_number, api_key):
    # Parse search string
    search_string = quote(search_string)
    # Create the search url
    query = "search/tv?api_key={}&page=1&query={}".format(api_key, search_string)
    result = tmdb(query)

    if result["results"]:
        tv_id = result["results"][0]["id"]

        query = "tv/{}/season/{}/episode/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, episode_number, api_key)
        result = tmdb(query)
    else:
        return None

    return result

def get_imdb_runtime(imdb_id):
    """ Get runtime from imdb in minutes.

    Args:
    imdb_id (string): Is the imdb id

    Returns:
    int: Runtime in minutes
    """

    # Define url
    url = "https://www.imdb.com/title/{}/".format(imdb_id)
    
    # Open the page and decode to html string
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # Parse html
    soup = BeautifulSoup(html, 'html.parser')
    title_bar_element = soup.find(attrs={"class": "titleBar"})
    time_element = title_bar_element.find("time")

    time_string = time_element.contents[0] 
    time_list = time_string.strip().split(" ")

    if len(time_list) == 2:
        hours = int(time_list[0].replace("h", ""))
        minutes = int(time_list[1].replace("min", ""))

        minutes = minutes + hours*60
    else:
        if "h" in time_list[0]:
            minutes = int(time_list[0].replace("h","")) * 60
        else:
            minutes = int(time_list[0].replace("min",""))

    return minutes

def get_episode_imdb_id(api_key, title, episode_name, season_number=None):
    """ Gets the IMDB id of a tv show episode

    Args:
        api_key (str): TMDB api key.
        title (str): Series title to search for.
        episode_name (str): Name of the episode. It has to be exactly the same name as in TMDB
        season_number (int): Number of the season. Optional but improves performance. 
    
    Returns:
        str/None: IMDB id of the episode or None if no match was found.

    """

    # Parse search string
    search_string = quote(title)
    # Create the search url
    query = "search/tv?api_key={}&page=1&query={}".format(api_key, search_string)
    result = tmdb(query)

    imdb_id = None

    if result["results"]:
        tv_id = result["results"][0]["id"]

        # Get tv series
        query = "tv/{}?api_key={}&append_to_response=external_ids".format(tv_id, api_key)
        result = tmdb(query)

        # Get number of seasons in series by looking at the last season number.
        # Some series have a bonus season which has the number 0
        number_of_seasons = result["seasons"][-1]["season_number"]
        

        # If a season number is provided
        if season_number:

            # Get the season
            query = "tv/{}/season/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, api_key)
            result = tmdb(query)

            # List of episodes
            episodes_in_season = result["episodes"]

            # Loop through episodes
            for ep in episodes_in_season:
                # If the name matches with the epsiode_name you are looking for
                if ep["name"].lower() == episode_name.lower():
                    # Episode number is defined
                    ep_number = ep["episode_number"]
                else:
                    ep_number = None
                
                # If the episode number is defined
                if ep_number:
                    # Search for the episode
                    query = "tv/{}/season/{}/episode/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, ep_number, api_key)
                    result = tmdb(query)

                    # Set the IMDB id
                    imdb_id = result["external_ids"]["imdb_id"]
                    # And break out of loop
                    break
                else: 
                    imdb_id = None
        # If the season number is not specified
        else: 
            # Loop through all season numbers
            for season_number in range(number_of_seasons):
                # If IMDB id has been found break out of loop
                if imdb_id:
                    break

                season_number = season_number + 1

                # Get the season
                query = "tv/{}/season/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, api_key)
                result = tmdb(query)
  
                # List of episodes
                episodes_in_season = result["episodes"]


                # Loop through episodes
                for ep in episodes_in_season:
                    # If the name matches with the epsiode_name you are looking for
                    if ep["name"].lower() == episode_name.lower():
                        # Episode number is defined
                        ep_number = ep["episode_number"]
                    else:
                        ep_number = None
                    
                    # If the episode number is defined
                    if ep_number:
                        # Search for the episode
                        query = "tv/{}/season/{}/episode/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, ep_number, api_key)
                        result = tmdb(query)

                        # Set the IMDB id
                        imdb_id = result["external_ids"]["imdb_id"]
                        # And break out of loop
                        break
                    else: 
                        imdb_id = None
                # imdb_id = None
    return imdb_id

def get_series_runtime(api_key, title):
     # Parse search string
    search_string = quote(title)
    # Create the search url
    query = "search/tv?api_key={}&page=1&query={}".format(api_key, search_string)
    result = tmdb(query)

    if result["results"]:
        tv_id = result["results"][0]["id"]

        # Get tv series
        query = "tv/{}?api_key={}&append_to_response=external_ids".format(tv_id, api_key)
        result = tmdb(query)

        runtime = result["episode_run_time"][0]
    else: 
        runtime = None

    return runtime





# API_KEY = get_api_key_from_file('tmdb-api-key.txt')
# print(get_series_runtime(API_KEY, "Suits"))
# print(get_episode_imdb_id(API_KEY, "Suits","She Knows"))
# print(search_movie("Rosenøen", get_api_key_from_file('tmdb-api-key.txt')))
# print(get_imdb_runtime("tt1973786"))
# print(get_episode("Suits", 1, 1, API_KEY)["external_ids"]["imdb_id"])
# print(get_episode("Suits", 1, 1, API_KEY))

