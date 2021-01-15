from flask import current_app as app
import re

def processRequestInput(requestInput, indices):
  imdbId=processImdbId(requestInput['imdbId'])
  print(imdbId)
  try:
    indices[imdbId]
    return imdbId
  except:
    errorMessage='Requested imdbId: {}, not available.'.format(requestInput['imdbId'])
    app.logger.error(errorMessage)
    return errorMessage

def processImdbId(id):
  regex = r"^tt\d{7}$"
  
  if re.search(regex, id):
    # strip tt and leading 0 + convert to int
    return int(re.sub(r"tt0*", "", id))
  else:
    raise ValueError('imdb id format is not supported')

def processReco(recommendations):
  # convert back imdbId int to proper value
  recommendations=recommendations.apply(updateImdbId)

  # conveting back to python list
  result = recommendations.values.tolist()

  return result

def updateImdbId(id):
  return "tt{}".format(str(id).zfill(7))

# def processDictInput(requestInput, ddbTable, indexName):
#   init = time.perf_counter()

#   rating_dict = {}

#   for row in requestInput:
#     try:
#       imdbId = processImdbId(row['imdbId'])
#       row.update({'imdbId': imdbId})
#     except:
#       app.logger.error('Wrong imdbId: {}, not taking it into account.'.format(row['imdbId']))
#       continue

#     try:
#       app.logger.info("searching for imdbId: {}".format(row['imdbId']))

#       items = ddbTable.query(
#         IndexName = indexName,
#         KeyConditionExpression=Key('imdbId').eq(row['imdbId'])
#       )['Items']

#       app.logger.info("items fetched: {}".format(items))
#     except botocore.exceptions.ClientError as error:
#       app.logger.error("ClientError from dynamoDB")
#       app.logger.error(error)
#       app.logger.error(error.response)

#     if len(items) > 0:
#       movieId = items[0]['movieId']

#       rating_dict.update({int(movieId): float(row['rating'])}) 
      
#       print("rating dict updated with:", movieId) 
#     else:
#       app.logger.error("No result found for imdbId:", row['imdbId'])

#   app.logger.info("Successfully processed request input in: {} seconds. Rating dict contains {} elements.".format(time.perf_counter() - init, len(rating_dict)))

#   app.logger.info(("dict: {}").format(rating_dict))

#   return rating_dict
