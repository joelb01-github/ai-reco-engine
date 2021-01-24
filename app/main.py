from flask import Flask, request
import lib.dataLoader as dl
import lib.dataMapper as mp
import lib.recommender as reco
import lib.utils as utils
import json
import os
import logging

app = Flask(__name__)

logging.basicConfig(
  level=os.environ['LOGGING_LEVEL'],
  format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

app.logger.info("Starting up the fire..")

with app.app_context(): # required as logger 
  df, cosine_sim = dl.loadData()
  indices = mp.getMapping(df)

@app.route('/reco-mvp', methods=['GET'])
def root():
  app.logger.info("Processing request at {}".format(request.path))
  return "Welcome to the Flask server"

@app.route('/reco-mvp/top-reco', methods=['POST'])
def topReco():
  app.logger.info("Processing request at {}".format(request.path))

  requestInput = json.loads(request.data)

  # Validate imdbId and check existence in data
  imdbId = utils.processRequestInput(requestInput, indices)

  # compute recommendation
  recommendations = reco.get_recommendations(imdbId, df, cosine_sim, indices)

  # Format results
  result = utils.processReco(recommendations)

  return json.dumps(result)
 
if __name__ == "__main__":
  app.logger.info("Running app in debugging mode")
  app.run(debug=True, port='5001', host='0.0.0.0')
