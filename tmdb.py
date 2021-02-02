import json
from urllib.request import urlopen
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
    # Replace space and & 
    search_string = search_string.replace(" ", "%20").replace("&", "%26")
    # Create the search url
    query = "search/movie?api_key={}&query={}&page=1".format(api_key, search_string)
    result = tmdb(query)
    
    movie_id = result["results"][0]["id"]

    query = "movie/{}?api_key={}".format(movie_id, api_key)
    result = tmdb(query)

    return result

def get_episode(search_string, season_number, episode_number, api_key):
     # Replace space and & 
    search_string = search_string.replace(" ", "%20").replace("&", "%26")
    # Create the search url
    query = "search/tv?api_key={}&page=1&query={}".format(api_key, search_string)
    result = tmdb(query)

    tv_id = result["results"][0]["id"]

    query = "tv/{}/season/{}/episode/{}?api_key={}&append_to_response=external_ids".format(tv_id, season_number, episode_number, api_key)
    result = tmdb(query)
    # print(result)
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
        hours = int(time_list[0].strip("h"))
        minutes = int(time_list[1].strip("min"))

        minutes = minutes + hours*60
    else:
        minutes = int(time_list[0].strip("min"))

    return minutes


# print(search_movie("Inception", get_api_key_from_file('tmdb-api-key.txt'))["runtime"])
# print(get_imdb_runtime("tt1973786"))
# print(get_episode("Suits", 1, 1, API_KEY)["external_ids"]["imdb_id"])
# print(get_episode("Suits", 1, 1, API_KEY))

