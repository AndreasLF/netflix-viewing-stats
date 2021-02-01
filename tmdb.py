import json
from urllib.request import urlopen

# Get API key for tmdb
with open('tmdb-api-key.txt') as f:
    json_data = json.load(f)
    API_KEY = json_data["api"]
    f.close()

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

    print(result)

# search_movie("Inception", API_KEY)


