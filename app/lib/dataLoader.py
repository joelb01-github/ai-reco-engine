from flask import current_app as app
import pandas as pd
import time
import os

def loadData():
  app.logger.info("loadData")
  init = time.perf_counter()

  INPUT_DIR='data/processedData'
  MOVIES_CSV_FILE = 'movies.csv'
  MOVIES_INPUT_PATH=os.path.join(INPUT_DIR, MOVIES_CSV_FILE)

  df=pd.read_csv(MOVIES_INPUT_PATH)

  app.logger.info("Successfully loaded dataset in: {} seconds.".format(time.perf_counter() - init))

  return df