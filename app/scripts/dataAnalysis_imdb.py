# Script to replace tmbd ID with imdb ID

import pandas as pd 
import numpy as np 
import os

def runProcessor():
  df=loadData()
  df=analysis(df)

def loadData():
  print("load Data")

  IMDB_INPUT_DIR='data/input/imdb'

  MOVIES_IMDB_CSV_FILE = 'movies_processed.csv'
  # MOVIES_IMDB_CSV_FILE = 'IMDb movies_small.csv'
  MOVIES_IMDB_INPUT_PATH=os.path.join(IMDB_INPUT_DIR, MOVIES_IMDB_CSV_FILE)

  columns=['imdb_title_id', 'genre', 'director', 'actors', 'keywords']

  df=pd.read_csv(
    MOVIES_IMDB_INPUT_PATH,
    dtype={
      'imdb_title_id': 'object',
      'genre': 'object',
      'director': 'object',
      'actors': 'object',
      'keywords': 'object'
    },
    usecols=columns
  )

  print("Data loaded.")
  return df

def analysis(df):
  # count nan
  print('count nan in keywords:', df['keywords'].isna().sum())
  print('count nan in imdb_title_id:', df['imdb_title_id'].isna().sum())
  print('count nan in genre:', df['genre'].isna().sum())
  print('count nan in actors:', df['actors'].isna().sum())
  print('count nan in director:', df['director'].isna().sum())

runProcessor()