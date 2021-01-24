from flask import current_app as app
import time

# Function that takes in movie title as input and outputs most similar movies

#   Get the index of the movie given its title.
#   Get the list of cosine similarity scores for that particular movie 
# with all movies. Convert it into a list of tuples where the first element
# is its position and the second is the similarity score.
#   Sort the aforementioned list of tuples based on the similarity scores; 
# that is, the second element.
#   Get the top 10 elements of this list. Ignore the first element as 
# it refers to self (the movie most similar to a particular movie is 
# the movie itself).
#   Return the titles corresponding to the indices of the top elements.

def get_recommendations(imdbId, df, cosine_sim, indices):
  app.logger.info("get_recommendations")
  init = time.perf_counter()

  # Get the index of the movie that matches the imdbId
  idx = indices[imdbId]

  # Get the pairwsie similarity scores of all movies with the requested one
  sim_scores = list(enumerate(cosine_sim[idx]))

  # Get the movie indices
  movie_indices = [i[1] for i in sim_scores]

  app.logger.info("Successfully created recommendations in: {} seconds.".format(time.perf_counter() - init))

  # Return the similar movies
  recommendations=df['imdbId'].iloc[movie_indices]

  print(recommendations.head())

  return recommendations