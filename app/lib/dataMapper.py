from flask import current_app as app
import time
import pandas as pd 

def getMapping(df):
  app.logger.info("getMapping")
  init = time.perf_counter()

  # Reset index of our main DataFrame
  df = df.reset_index()

  # Construct reverse mapping
  indices = pd.Series(df.index, index=df['imdbId'])

  app.logger.info("Successfully created the mapping in: {} seconds.".format(time.perf_counter() - init))

  return indices