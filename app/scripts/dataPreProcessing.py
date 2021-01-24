# Script to replace tmbd ID with imdb ID

import pandas as pd 
import numpy as np 
import os
from ast import literal_eval

def runProcessor():
  df=loadData()
  df=processData(df)
  writeData(df)

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

def processData(df):
  # replace na values with []
  df=df.fillna(value=str([]),axis=1)

  # change string from "x, y, z" to [x, y, z]
  features = ['genre', 'director', 'actors']
  for feature in features:
      df[feature] = df[feature].apply(formatStrToList)

  # reformat keywords from "[{id: 2, name: x}, ...]" to [x, ...]
  df['keywords']=df['keywords'].apply(formatDeepListToList)

  # Rename colums
  data=df.rename(columns={
    'imdb_title_id':'imdbId',
    'director': 'directors',
    'genre': 'genres'
  })

  print("Data processed.")
  return data

# Changes a string to a list with the tmdb formatting
def formatStrToList(x):
  return str(x).split(', ')

def formatDeepListToList(x):
  if not isinstance(x, str):
    return str([])

  obj=literal_eval(x)
  keywords = [i['name'] for i in obj]

  return keywords

def writeData(data):
  OUTPUT_DIR='data/processedData'
  OUTPUT_FILE='movies.csv'
  OUTPUT_PATH=os.path.join(OUTPUT_DIR, OUTPUT_FILE)

  data.to_csv(OUTPUT_PATH,index=False)

  print("Data written to disk.")

runProcessor()