import pandas as pd
import datetime


movies_data = "netflix_movies_runtime.csv"

movies_df = pd.read_csv(movies_data)

# Convert date column to datetime object
movies_df["Date"] =  pd.to_datetime(movies_df['Date'], format='%d/%m/%Y')

# Total amount of movies watched
total_movies = len(movies_df)

# Get date of the first movie watched
first_movie_date = movies_df["Date"].min()
# Get alle the episodes you watched on the day you started watching Netflix
all_first_movies = movies_df[movies_df["Date"]==first_movie_date]
try: 
    all_first_movies_joined = "\n- ".join(all_first_movies["Title"])
except: 
    all_first_movies_joined = all_movies_episodes["Title"]


today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond= 0)
days_since_first_movie = (today - first_movie_date).days

# first_movie_date = datetime.date(movies_df.iloc[-1,2])

# Count NaN values 
nans = movies_df["runtime"].isna().sum()

# Drop the NaN values
movies_df = movies_df.dropna()

# Calculate runtime
runtime = sum(movies_df["runtime"])
runtime_hours = runtime // 60
runtime_minutes = runtime % 60


# daily average

print()
print("MOVIES")
print("-"*100)
print("You watched your first movie on {} \nOn this day you watched the following movie(s): \n- {}".format(first_movie_date.date(), all_first_movies_joined))
# print("You watched the first movie, '{}', on {}".format(movies_df.iloc[-1,1], first_movie_date.date()))
print()
print("You have watched {} movies on Netflix since then (not counting duplicates)".format(total_movies))
print("This adds up to a total of {} hours and {} minutes".format(runtime_hours, runtime_minutes))
print()
print("(Data is missing on {} movies, which is {:.2f} % of the total amount of movies)".format(nans, (nans/total_movies)*100))
print()
print("On average you have spent {:.2f} minutes each day watching Netflix movies".format(runtime/days_since_first_movie))
print()
print("Assuming all the movies with missing data have a runtime equal to the average runtime of alle the other movies:")
movies_runtime_estimate = (runtime/days_since_first_movie)/(1-(nans/total_movies))
print("On average you have spent {:.2f} minutes each day watching Netflix movies".format(movies_runtime_estimate))
print("-"*100)
print()



series_data = "netflix_series_runtime.csv"


series_df = pd.read_csv(series_data)


series_df["Date"] =  pd.to_datetime(series_df['Date'], format='%d/%m/%Y')

# Total amount of movies watched
total_episodes = len(series_df)


# Get date of the first movie watched
first_episode_date = series_df["Date"].min()
# Get alle the episodes you watched on the day you started watching Netflix
all_first_episodes = series_df[series_df["Date"]==first_episode_date]
try: 
    all_first_episodes_joined = "\n- ".join(all_first_episodes["Title"])
except: 
    all_first_episodes_joined = all_first_episodes["Title"]



today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond= 0)
days_since_first_episode = (today - first_episode_date).days

# Count NaN values 
nans = series_df["runtime"].isna().sum()

# Drop the NaN values
series_df = series_df.dropna()

# Calculate runtime
runtime = sum(series_df["runtime"])
runtime_hours = runtime // 60
runtime_minutes = runtime % 60


# daily average
print()
print("SERIES")
print("-"*100)
print("You watched your first episode on {} \nOn this day you watched the following episode(s): \n- {}".format(first_episode_date.date(), all_first_episodes_joined)
)
print()
print("You have watched {} episodes on Netflix since then (not counting duplicates)".format(total_episodes))
print("This adds up to a total of {:.0f} hours and {:.0f} minutes".format(runtime_hours, runtime_minutes))
print()
print("(Data is missing on {} episodes, which is {:.0f} % of the total amount of episodes watched)".format(nans, (nans/total_episodes)*100))
print()
print("On average you have spent {:.0f} minutes each day watching Netflix series".format(runtime/days_since_first_movie))
print()
print("Assuming all the episodes with missing data have a runtime equal to the average runtime of alle the other episodes:")
series_runtime_estimate = (runtime/days_since_first_episode)/(1-(nans/total_episodes))
print("On average you have spent {:.2f} minutes each day watching Netflix movies".format(series_runtime_estimate))
print("-"*100)
print()
print("Conclusion: ")
print("Your estimated daily time spent on Netflix is {:.2f} minutes".format(series_runtime_estimate+movies_runtime_estimate))
print()
print("This is a rough estimate, since Netflix do not provide very useful data; only title and date. \nDuplicates are not included in the data. \nData is retrieved from TDMB or scraped from Netflix, which also results in faulty data, \nsince some movies have similar or translated names or simply do not exist in the databases")
print()


