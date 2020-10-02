from flask import Flask, request
import json

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/reco-mvp', methods=['GET'])
def root():
  print('healtcheck OK')
  return "Welcome to the Flask server"

@app.route('/reco', methods=['POST'])
def reco():
  data = json.loads(request.data)

  recommendations = 'call function here'

  return json.dumps(recommendations)
 
if __name__ == "main":
    app.run(debug=True, port='5001', host='0.0.0.0')
