from flask import Flask, request
import lib.useruser_reco as reco
import lib.utils as utils
import json
import boto3
import os
import logging

app = Flask(__name__)

logging.basicConfig(
  level=os.environ['LOGGING_LEVEL'],
  format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

app.logger.info("Starting up the fire..")

dynamodb = boto3.resource('dynamodb')
linksTableName = os.environ['LINKS_TABLE']
indexName = os.environ['INDEX_NAME']

try:
  ddbTable = dynamodb.Table(linksTableName)
except:
  app.logger.error("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

data = reco.loadData()
algo = reco.initialiseEngine(data)

@app.route('/reco-mvp', methods=['GET'])
def root():
  app.logger.info("Processing request at {}".format(request.path))

  return "Welcome to the Flask server"

@app.route('/reco-mvp/top-reco', methods=['POST'])
def topReco():
  app.logger.info("Processing request at {}".format(request.path))

  requestInput = json.loads(request.data)

  rating_dict = utils.processRequestInput(requestInput, ddbTable, indexName)

  recommendations = reco.getReco(algo, data, rating_dict)

  result = utils.processReco(recommendations)

  return json.dumps(result)
 
if __name__ == "__main__":
  app.logger.info("Running app in debugging mode")
  app.run(debug=True, port='5001', host='0.0.0.0')
