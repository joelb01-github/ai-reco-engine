from flask import current_app as app
import lenskit.datasets as ds
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
import time

def loadData():
  init = time.perf_counter()

  data = ds.MovieLens('data/ML-Latest-Small')

  app.logger.info("Successfully loaded ML datasets in: {} seconds.".format(time.perf_counter() - init))

  return data

def initialiseEngine(data):
  init = time.perf_counter()

  # minimum and maximum number of neighbors to consider ("reasonable defaults")
  min_neighbors = 3
  max_neighbors = 15

  user_user = UserUser(max_neighbors, min_nbrs=min_neighbors)
  algo = Recommender.adapt(user_user)
  algo.fit(data.ratings)

  app.logger.info("User-User algorithm all set up in: {} seconds.".format(time.perf_counter() - init))

  return algo

def getReco(algo, data, rating_dict):
  init = time.perf_counter()

  # number of recommendations to generate
  num_recs = 10

  recs = algo.recommend(-1, num_recs, ratings=pd.Series(rating_dict))  # -1 tells it that it's not an existing user in the set e.g. we're giving new ratings

  recommendations = recs.join(data.movies['genres'], on='item')      
  recommendations = recommendations.join(data.movies['title'], on='item')
  recommendations = recommendations.join(data.links['imdbId'], on='item')
  print(recommendations)
  recommendations = recommendations[recommendations.columns[2:]]

  app.logger.info("Successfully computed recommendations in: {} seconds.".format(time.perf_counter() - init))

  app.logger.info("\n\nRECOMMENDED:")
  app.logger.info(recommendations)

  return recommendations
