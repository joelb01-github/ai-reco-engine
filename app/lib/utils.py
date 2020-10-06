import pandas as pd
import time
import botocore
from boto3.dynamodb.conditions import Key

def processRequestInput(requestInput, ddbTable, indexName):
  init = time.perf_counter()

  rating_dict = {}

  for row in requestInput:
    try:
      print("searching for imdbId:", row['imdbId'])
      items = ddbTable.query(
        IndexName = indexName,
        KeyConditionExpression=Key('imdbId').eq(row['imdbId'])
      )['Items']
      print("items fetched:", items)
    except botocore.exceptions.ClientError as error:
      print("ClientError from dynamoDB")
      print(error)
      print(error.response)

    if len(items) > 0:
      movieId = items[0]['movieId']
      rating_dict.update({int(movieId): float(row['rating'])}) 
      print("rating dict updated with:", movieId) 
    else:
      print("No result found for imdbId:", row['imdbId'])
          
  print("Successfully processed request input in:", time.perf_counter() - init, "seconds. Rating dict contains", len(rating_dict), "elements.")

  print("dict:", rating_dict)

  return rating_dict

def processReco(recommendations):
  result = recommendations.to_dict('records')

  return result
