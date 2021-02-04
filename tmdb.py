from googlesearch import search
import json
from urllib.request import urlopen
from urllib.parse import quote
import re
from bs4 import BeautifulSoup
import time

class NetflixMovie:
    """ Netflix movie containing movie title and the date it was watched.

    Args:
        movie_title (str): The title of the movie.
        date_watched (str): The date the movie was watched.

    Attributes:
        title (str): Movie title.
        date_watched (int): The date the movie was watched.
        self.API_KEY (str): TMDB API_KEY
    """
    def __init__(self, movie_title, date_watched): 
        self.title = movie_title
        self.date_watched = date_watched


    def set_tmdb_api_key_from_file(self, path):
        """ Set the TMDB API key from file. Has to be json format.

        Args:
            path (str): Txt file path.
        """
        with open(path) as f:
            json_data = json.load(f)
            self.API_KEY = json_data["api"]
            f.close()
    
    def __tmdb_query(self, query):
        """Make TMDB api request.

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

    def __search_movie(self, search_string, number_of_search = 1):
        """ Search for movie on TMDB.

        Args:
            search_string (str): What to search for, should be the title of the movie.
            number_of_search (str): If multiple search results exist, this allows you to specifiy which movie to pick from the list. Default: picks the first result from the list

        Returns:
            json: The result of the TMDB search

        """
        api_key = self.API_KEY

        # Parse search string
        search_string = quote(search_string)
        # Create the search url
        query = "search/movie?api_key={}&query={}&page=1".format(api_key, search_string)
        result = self.__tmdb_query(query)
        
        if result["results"]:
            try:
                movie_id = result["results"][number_of_search-1]["id"]
            except:
                movie_id = result["results"][0]["id"]

            query = "movie/{}?api_key={}".format(movie_id, api_key)
            result =  self.__tmdb_query(query)
        else:
            return None

        return result

    
    def get_netflix_english_title(self):
        """ Try to scrape the title from Netflix and get the english translation.

        First a Google search is made on Netflix' site and then the Netflix id is obtained and the English 
        translated site is accessed and scraped.

        Returns:
            The English title found on Netflix
        """
        title = self.title

        # Make a google search on netlfix.com
        query = '{} site:netflix.com'.format(title)
        result = search(query, lang="en")

        if result:
            # Take the first url
            url = result[0]

            r = re.findall("https://www.netflix.com/(.*)/title/(.*)", url)

            # If site is not as expected return None
            try:
                netflix_id = r[0][1]
            except:
                return None

            # Create new url
            url = "https://www.netflix.com/dk-en/title/{}".format(netflix_id)
            
            # Open the page and decode to html string
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")

            # Parse html
            soup = BeautifulSoup(html, 'html.parser')
            # Find the title element
            title_element = soup.find(attrs={"class": "title-title"})
            english_title = title_element.contents[0]
        else:
            english_title = None

        return english_title

    def get_netflix_runtime(self):
        """ Try to scrape the runtime from Netflix.

        First a Google search is made on Netflix' site and then the runtime is scraped from the first search result

        Returns:
            The English title found on Netflix
        """
        title = self.title

        # Make a google search on netlfix.com
        query = '{} site:netflix.com'.format(title)
        result = search(query, lang="en")

        if result:
            # Take the first url
            url = result[0]
            
            # Check if url matches the correct format
            r = re.findall("https://www.netflix.com/(.*)/title/(.*)", url)
            if not r:
                return None 

            # Open the page and decode to html string
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")

            # Parse html
            soup = BeautifulSoup(html, 'html.parser')
            # Find the title element
            runtime_element = soup.find(attrs={"class": "duration"})
            time_string = runtime_element.contents[0]

            try: 
                time_list = time_string.strip().split(" t. ")
                hours = int(time_list[0])
                minutes = int(time_list[1].replace(" min.", ""))
                runtime = minutes + hours*60
            except:
                runtime = int(time_list[1].replace(" min.", ""))
        else:
            runtime = None
        return runtime

    def get_movie_runtime(self, scrape_netflix = False):
        """ Get the movie runtime.

        Args:
            scrape_netlfix (bool): Scrape Netflix if no match is found on TMDB, time consuming and does not guarantee a result.

        Returns:
            int: Movie runtime in minutes. None if no runtime was found
        """
        title = self.title
        API_KEY = self.API_KEY

        result = self.__search_movie(title, API_KEY)

        # If a result has been retrieved the runtime is set
        if result:
            runtime = int(result["runtime"])
            
        else:
            # Is Netflix scraping set
            if scrape_netflix:   
               runtime = self.get_netflix_runtime()
            else:
                runtime = None
        
        return runtime

   
time1 = time.time()

movie = NetflixMovie("Rosenøen", "Date")
movie.set_tmdb_api_key_from_file("tmdb-api-key.txt")
movie.allow_netflix_scraping = True
title = movie.get_movie_runtime(True)

print(time.time() - time1)

print(title)

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
# print(get_movie_runtime("inception",API_KEY))
# print(get_series_runtime(API_KEY, "Suits"))
# print(get_episode_imdb_id(API_KEY, "Suits","She Knows"))
# print(search_movie("Rosenøen", get_api_key_from_file('tmdb-api-key.txt')))
# print(get_imdb_runtime("tt1973786"))
# print(get_episode("Suits", 1, 1, API_KEY)["external_ids"]["imdb_id"])
# print(get_episode("Suits", 1, 1, API_KEY))

