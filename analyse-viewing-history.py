import pandas as pd

file_path = "NetflixViewingHistory.csv"

df = pd.read_csv(file_path)
# print(df)

ts = pd.Series(df['Title'].values)

# Classify if it is a series or a movie based on the colons in the title
df["type"] = ["series" if len(y.split(":")) >= 3 else "movie" for y in df["Title"]]


# print(df.head)
