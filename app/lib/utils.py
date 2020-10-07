from flask import current_app as app
import pandas as pd
import time
import botocore
from boto3.dynamodb.conditions import Key

def processRequestInput(requestInput, ddbTable, indexName):
  init = time.perf_counter()

  rating_dict = {}

  for row in requestInput:
    try:
      app.logger.info("searching for imdbId: {}".format(row['imdbId']))
      items = ddbTable.query(
        IndexName = indexName,
        KeyConditionExpression=Key('imdbId').eq(row['imdbId'])
      )['Items']
      app.logger.info("items fetched: {}".format(items))
    except botocore.exceptions.ClientError as error:
      app.logger.error("ClientError from dynamoDB")
      app.logger.error(error)
      app.logger.error(error.response)

    if len(items) > 0:
      movieId = items[0]['movieId']
      rating_dict.update({int(movieId): float(row['rating'])}) 
      print("rating dict updated with:", movieId) 
    else:
      app.logger.error("No result found for imdbId:", row['imdbId'])

  app.logger.info("Successfully processed request input in: {} seconds. Rating dict contains {} elements.".format(time.perf_counter() - init, len(rating_dict)))

  app.logger.info("dict:", rating_dict)

  return rating_dict

def processReco(recommendations):
  result = recommendations.to_dict('records')

  return result
