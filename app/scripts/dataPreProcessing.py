# Script to replace tmbd ID with imdb ID

import pandas as pd 
import numpy as np 
import os

print("load Data")

TMDB_INPUT_DIR='data/tmdb'
MOVIES_CSV_FILE = 'tmdb_5000_movies.csv'
MOVIES_INPUT_PATH=os.path.join(TMDB_INPUT_DIR, MOVIES_CSV_FILE)
CREDITS_CSV_FILE = 'tmdb_5000_credits.csv'
CREDITS_INPUT_PATH=os.path.join(TMDB_INPUT_DIR, CREDITS_CSV_FILE)

MLENS_INPUT_DIR='data/movielens'
LINKS_CSV_FILE = 'links.csv'
LINKS_INPUT_PATH=os.path.join(MLENS_INPUT_DIR, LINKS_CSV_FILE)

df1=pd.read_csv(CREDITS_INPUT_PATH)
df2=pd.read_csv(MOVIES_INPUT_PATH)
links=pd.read_csv(LINKS_INPUT_PATH)

print("Data loaded.")

# join the two dataset on the 'tmdbId' column
df1.columns = ['tmdbId','tittle','cast','crew']
df2.rename(columns={'id':'tmdbId'}, inplace=True)
data = df2.merge(df1,on='tmdbId')
data = data.merge(links,on='tmdbId')

print("Data processed.")

OUTPUT_DIR='data/processedData'
OUTPUT_FILE='movies.csv'
OUTPUT_PATH=os.path.join(OUTPUT_DIR, OUTPUT_FILE)

data.to_csv(OUTPUT_PATH,index=False)

print("Data written to disk.")