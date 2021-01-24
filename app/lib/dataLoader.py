from flask import current_app as app
import pandas as pd
import time
import os
import pickle

def loadData():
  app.logger.info("loadData")
  init = time.perf_counter()

  INPUT_DIR_DATA='data/processedData'
  MOVIES_CSV_FILE = 'movies.csv'
  MOVIES_INPUT_PATH=os.path.join(INPUT_DIR_DATA, MOVIES_CSV_FILE)

  df=pd.read_csv(MOVIES_INPUT_PATH)

  INPUT_DIR_MODEL='data/model'
  COSINE_SIM_MATRIX = 'cosine_sim_matrix.pkl'
  MODEL_PATH=os.path.join(INPUT_DIR_MODEL, COSINE_SIM_MATRIX)

  with open(MODEL_PATH, 'rb') as file:
    cosine_sim = pickle.load(file)

  app.logger.info("Successfully loaded data in: {} seconds.".format(time.perf_counter() - init))

  return df, cosine_sim