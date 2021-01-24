from flask import current_app as app
import re

def processRequestInput(requestInput, indices):
  app.logger.info('processRequestInput')

  imdbId=requestInput['imdbId']

  verifyImdbFormat(imdbId)

  try:
    indices[imdbId]
    return imdbId
  except:
    errorMessage='Requested imdbId: {}, not available.'.format(requestInput['imdbId'])
    app.logger.error(errorMessage)
    return errorMessage

def verifyImdbFormat(id):
  regex = r"^tt\d{7}$"
  
  if re.search(regex, id):
    return 
  else:
    raise ValueError('wrong imdb id format.')

def processReco(recommendations):
  app.logger.info('processReco')

  # conveting back to python list
  result = {
    "results": recommendations.values.tolist()
  }

  return result
