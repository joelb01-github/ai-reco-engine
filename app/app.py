from flask import Flask, request
import json

app = Flask(__name__, static_folder='.', static_url_path='')

jsonInput = '[ {"movieId": 3, "rating": 4.0}, {"movieId": 6, "rating": 4.0}, {"movieId": 47, "rating": 5.0}, {"movieId": 50, "rating": 5.0}, {"movieId": 70, "rating": 3.0}, {"movieId": 101, "rating": 5.0}, {"movieId": 110, "rating": 4.0}, {"movieId": 151, "rating": 5.0}, {"movieId": 157, "rating": 5.0}, {"movieId": 163, "rating": 5.0} ]'

data = loadData()
algo = initialiseEngine(data)

@app.route('/reco-mvp', methods=['GET'])
def root():
  print('healtcheck OK')
  return "Welcome to the Flask server"

@app.route('/reco-mvp/top-reco', methods=['POST'])
def reco():
  requestInput = json.loads(request.data)

  recommendations = getReco(algo, data, requestInput)

  return json.dumps(recommendations)
 
if __name__ == "__main__":
    app.run(debug=True, port='5001', host='0.0.0.0')
