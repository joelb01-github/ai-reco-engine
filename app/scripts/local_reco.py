import time
import os
import pickle
import pandas as pd 

def constructIndeces(df):
  # Construct reverse mapping
  print("Construct reverse mapping")
  indices = pd.Series(df.index, index=df['imdbId'])

  return indices

def loadData():
  print("loadData")
  init = time.perf_counter()

  INPUT_DIR='data/processedData'
  MOVIES_CSV_FILE = 'movies.csv'
  # MOVIES_CSV_FILE = 'movies_small.csv'
  MOVIES_INPUT_PATH=os.path.join(INPUT_DIR, MOVIES_CSV_FILE)

  df=pd.read_csv(MOVIES_INPUT_PATH)

  print("Successfully loaded dataset in: {} seconds.".format(time.perf_counter() - init))

  return df

def readData():
  INPUT_DIR='data/model'
  COSINE_SIM_MATRIX = 'cosine_sim_matrix.pkl'
  MODEL_PATH=os.path.join(INPUT_DIR, COSINE_SIM_MATRIX)

  with open(MODEL_PATH, 'rb') as file:
    cosine_sim = pickle.load(file)

  return cosine_sim

print("get_recommendations")
init = time.perf_counter()

df=loadData()
cosine_sim=readData()
indices=constructIndeces(df)

imdbId='tt0480702'

# Get the index of the movie that matches the imdbId
idx = indices[imdbId]

# Get the pairwsie similarity scores of all movies with the requested one
sim_scores = list(enumerate(cosine_sim[idx]))

# Get the movie indices
movie_indices = [i[1] for i in sim_scores]

print("Successfully created recommendations in: {} seconds.".format(time.perf_counter() - init))

# Return the top 10 most similar movies
recommendations=df['imdbId'].iloc[movie_indices]

print(recommendations.head())