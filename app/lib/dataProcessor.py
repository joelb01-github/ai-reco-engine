from flask import current_app as app
import time
import pandas as pd 
import numpy as np 
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def processData(df):
    app.logger.info("processData")
    app.logger.info("debug0")
    init = time.perf_counter()
    app.logger.info("debug00")

    # we need to extract the three most important actors, the director and the keywords associated with that movie. Right now, our data is present in the form of "stringified" lists , we need to convert it into a safe and usable structure

    # Parse the stringified features into their corresponding python objects

    features = ['cast', 'crew', 'keywords', 'genres']
    app.logger.info("debug000")
    for feature in features:
        df[feature] = df[feature].apply(literal_eval)

    app.logger.info("debug1")

    # Define new director, cast, genres and keywords features that are in a suitable form.
    df['director'] = df['crew'].apply(get_director)

    app.logger.info("debug2")

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df[feature] = df[feature].apply(get_list)


    app.logger.debug("debug3")

    # # Print the new features of the first 3 films
    # print(df[['title', 'cast', 'director', 'keywords', 'genres']].head(3))

    # Apply clean_data function to your features. This is done so that our vectorizer doesn't count the Johnny of "Johnny Depp" and "Johnny Galecki" as the same.
    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        df[feature] = df[feature].apply(clean_data)

    app.logger.debug("debug4")

    # create our "metadata soup"
    df['soup'] = df.apply(create_soup, axis=1)

    app.logger.debug("debug5")

    # create the count matrix. we use the CountVectorizer() instead of TF-IDF. This is because we do not want to down-weight the presence of an actor/director if he or she has acted or directed in relatively more movies. It doesn't make much intuitive sense.
    count = CountVectorizer(stop_words='english')

    app.logger.debug("debug6")
    count_matrix = count.fit_transform(df['soup'])

    app.logger.debug("debug7")

    # Compute the Cosine Similarity matrix based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    app.logger.debug("debug8")

    # Reset index of our main DataFrame and construct reverse mapping
    df = df.reset_index()
    indices = pd.Series(df.index, index=df['imdbId'])

    app.logger.debug("debug9")

    app.logger.info("Successfully processed the data in: {} seconds.".format(time.perf_counter() - init))

    return cosine_sim, indices

# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# Function to convert all strings (names and keyword instances) to lower case and strip spaces between them.
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

# Creates a string that contains all the metadata that we want to feed to our vectorizer (namely actors, director and keywords).
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])