import pandas as pd
import re
from tmdb import NetflixMovie, NetflixSeries
from scrape_netflix import get_english_title
import time

# Get the api key from file
# API_KEY = tmdb.get_api_key_from_file('tmdb-api-key.txt')

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

def set_series_title(row):
    title, episode, season = series_name_split(row["Title"])
    return title

def set_runtime(row):
    # Check if it is a movie
    if row["type"] == "movie":
        print(row["Title"])
        movie = NetflixMovie(row["Title"],row["Date"])
        movie.set_tmdb_api_key_from_file("tmdb-api-key.txt")
        runtime = movie.get_movie_runtime(True)
    else:
        pass
        # title, episode, season = series_name_split(row["Title"])
        # imdb_id = tmdb.get_episode_imdb_id(API_KEY, title, episode, season)

        # if imdb_id:
        #     runtime = tmdb.get_imdb_runtime(imdb_id)
        # else: 
        # runtime = tmdb.get_series_runtime(API_KEY, title)
        
    return runtime

def create_movies_csv(df):
    # Only look at the movies
    df = df[df['type'] == "movie"]
    # df = df.iloc[:5,:]

    # Set the runtime column
    df["runtime"] = df.apply(set_runtime, axis=1)
    # df = df.dropna()

    # Print time it took
    print(time.time() - time1)

    # Write results to a csv file
    df.to_csv("netflix_movies_runtime.csv")

def create_series_csv(df):
    # Only look at series
    df = df[df['type'] == "series"]
    # df = df.iloc[:10,:]


    df["series_title"] = df.apply(set_series_title, axis=1)

    grouped = df.groupby("series_title")
    # df["runtime"] = df.apply(set_runtime, axis=1)

    df_new = pd.DataFrame(columns = ["Title", "Date", "type", "series_title", "runtime"])
    for name, group in grouped:
        # Create series object and get the runtime
        series = NetflixSeries(name)
        series.set_tmdb_api_key_from_file("tmdb-api-key.txt")
        runtime = series.get_runtime()

        # # Set the episode runtime for the whole group
        group["runtime"] = runtime

        df_new = df_new.append(group)
        print(name)


    df_new.to_csv("netflix_series_runtime.csv")





# track time spent
time1 = time.time()

file_path = "NetflixViewingHistory.csv"

df = pd.read_csv(file_path)

# Classify if it is a series or a movie based on the colons in the title
df["type"] = ["series" if len(y.split(":")) >= 3 else "movie" for y in df["Title"]]

create_movies_csv(df)

print("It took {} minutes to finish".format(time.time() - time1))
