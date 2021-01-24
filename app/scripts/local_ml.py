import time
import pandas as pd 
import numpy as np
import os
import pickle
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def processData(df):
  print("processData")
  init = time.perf_counter()

  features = ['directors', 'actors', 'keywords', 'genres']
  for feature in features:
    # convert "stringified" lists into a safe and usable structure
    df[feature] = df[feature].apply(literal_eval)

    # extract the three most important items
    df[feature] = df[feature].apply(get_list)

    # clean_data so that the vectorizer doesn't count the Johnny of "Johnny Depp" and "Johnny Galecki" as the same.
    df[feature] = df[feature].apply(clean_data)
    
  # create our "metadata soup"
  print("create our metadata soup")
  df['soup'] = df.apply(create_soup, axis=1)
  
  # CountVectorizer() used instead of TF-IDF so that we do not down-weight the presence of an actor/director if he or she has acted or directed in relatively more movies.
  print("Vectorizing")
  count = CountVectorizer(stop_words='english')

  # create the count matrix.
  print("create the count matrix.")
  count_matrix = count.fit_transform(df['soup'])

  print(count_matrix.shape)

  # Compute the Cosine Similarity matrix based on the count_matrix
  cosine_sim = cosine_similarity_n_space(count_matrix)
  print('cosine_sim.shape[0]', cosine_sim.shape[0])

  # Reset index of the main DataFrame
  print("Reset index of our main DataFrame")
  df = df.reset_index()

  # Construct reverse mapping
  print("Construct reverse mapping")
  indices = pd.Series(df.index, index=df['imdbId'])

  print("Successfully processed the data in: {} seconds.".format(time.perf_counter() - init))

  return cosine_sim, indices

def cosine_similarity_n_space(matrix, batch_size=1000, top=100):
  # Compute the maximum number of recommendations between top and the size of matrix
  max_size=min(matrix.shape[0], top)
  print('matrix.shape[0]', matrix.shape[0])
  print('max_size', max_size)

  ret = np.ndarray((matrix.shape[0], max_size-1))

  batch_numbers=int(matrix.shape[0] / batch_size) + 1
  print('batch_numbers', batch_numbers)

  for batch_i in range(0, batch_numbers):
    print('batch_i', batch_i)

    start = batch_i * batch_size
    # print('start', start)
    end = min([(batch_i + 1) * batch_size, matrix.shape[0]])
    # print('end', end)

    if end <= start:
        break # cause I'm too lazy to elegantly handle edge cases

    rows = matrix[start: end]
    sim = cosine_similarity(rows, matrix) # rows is O(1) size

    # print('sim not sorted', sim)

    for count, value in enumerate(range(start, end)):
      # print('count', count)
      # print('value', value)

      # Get the pairwsie similarity scores of all movies with the requested one
      sim_scores = sim[count]
      # print('sim_scores', sim_scores)

      # Sort the scores and extract the respective indexes
      sorted_indexes_asc=np.argsort(sim_scores)
      # print('sorted_indexes_asc', sorted_indexes_asc)
      sorted_indexes_desc=np.flip(sorted_indexes_asc)
      # print('sorted_indexes_desc', sorted_indexes_desc)

      # Only keep the top indexes
      sorted_indexes_desc = sorted_indexes_desc[1:max_size]
      # print('sorted_indexes_desc cut', sorted_indexes_desc)

      # add to final result
      ret[value] = sorted_indexes_desc
      # print('ret i', ret)
  return ret

# Save to file in the current working directory
def writeData(cosine_sim):
  OUTPUT_DIR='data/model'
  COSINE_SIM_MATRIX = 'cosine_sim_matrix.pkl'
  OUTPUT_PATH=os.path.join(OUTPUT_DIR, COSINE_SIM_MATRIX)

  with open(OUTPUT_PATH, 'wb') as file:
    pickle.dump(cosine_sim, file)

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
  if isinstance(x, list):
      #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
      if len(x) > 3:
          x = x[:3]
      return x

  #Return empty list in case of missing/malformed data
  return []

# Function to convert all strings (names and keyword instances) to lower case and strip spaces between them.
def clean_data(x):
  if isinstance(x, list):
      return [str.lower(i.replace(" ", "")) for i in x]

# Creates a string that contains all the metadata that we want to feed to our vectorizer (namely actors, director and keywords).
def create_soup(x):
  soup=' '.join(x['keywords']) + ' ' + ' '.join(x['actors']) + ' ' + ' '.join(x['directors']) + ' ' + ' '.join(x['genres'])
  return soup

df = loadData()
cosine_sim, indices = processData(df)
writeData(cosine_sim)

print('Model processing finalised.')