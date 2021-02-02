import pandas as pd
import re
import tmdb
from scrape_netflix import get_english_title

# Get the api key from file
API_KEY = tmdb.get_api_key_from_file('tmdb-api-key.txt')

pd.set_option('display.max_rows', 1000)

def series_name_split(title):
    if "Sæson" in title:
        r = re.split(": Sæson [0-9]*: ", title)
        season_number = int(re.findall("(.*)(Sæson )([0-9]*)(.*)", title)[0][2])
        tv_show_title = r[0]
        episode_name = r[1]
    elif "Season" in title:
        r = re.split(": Season [0-9]*: ", title)
        season_number = int(re.findall("(.*)(Season )([0-9]*)(.*)", title)[0][2])
        tv_show_title = r[0]
        episode_name = r[1]

    else:
        title_split = title.split(":")

        tv_show_title = ":".join(title_split[:-2])
        episode_name = title_split[-1].strip()
        season_number = None
   
    # imdb_id = tmdb.get_episode_imdb_id()

    return (tv_show_title, episode_name, season_number)

def set_runtime(row):
    # Check if it is a movie
    if row["type"] == "movie":
        # Search TMDB for the title
        result = tmdb.search_movie(row["Title"], API_KEY)

        # If a result has been retrieved the runtime is set
        if result:
            runtime = result["runtime"]
        else:
            # # Netflix will be scraped for the English title
            # english_title = get_english_title(row["Title"])
            # # If an English title was found
            # if english_title:    
            #     # Search on TMDB again
            #     result = tmdb.search_movie(english_title, API_KEY)
            #     if result:
            #         # If the result contains anything runtime will be set
            #         runtime = result["runtime"]
            #     else:
            #         # If not runtime is undefined
            #         runtime = None
            # else: 
            #     runtime = None
            runtime = None
    else:
        title, episode, season = series_name_split(row["Title"])
        # imdb_id = tmdb.get_episode_imdb_id(API_KEY, title, episode, season)

        # if imdb_id:
        #     runtime = tmdb.get_imdb_runtime(imdb_id)
        # else: 
        runtime = tmdb.get_series_runtime(API_KEY, title)
        
    return runtime

file_path = "NetflixViewingHistory.csv"

df = pd.read_csv(file_path)

# ts = pd.Series(df['Title'].values)

# Classify if it is a series or a movie based on the colons in the title
df["type"] = ["series" if len(y.split(":")) >= 3 else "movie" for y in df["Title"]]

df = df[df['type'] == "movie"]
# df = df.iloc[:5,:]


df["runtime"] = df.apply(set_runtime, axis=1)
df = df.dropna()


print(sum(df["runtime"]))



# for index, row in df.iterrows():
#     # print(row["Title"])
#     if row["type"] == "movie":
#         result = tmdb.search_movie(row["Title"], tmdb.get_api_key_from_file('tmdb-api-key.txt'))
#         if result:
#             runtime = result["runtime"]
#         else:
#             runtime = None
#     else:
#         runtime = None
    
#     print(runtime)

    # else:
    #     print("Series")


# df["series_name"] = ["S" if df["type"] == "series" else None for y in df["Title"]]



title, episode, season = series_name_split("Spartacus: Blood and Sand: Vengeance: Wrath of the Gods")
# print(title, episode, season)
# print(df.head)
