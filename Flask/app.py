from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='demo.log', level=logging.DEBUG)

@app.route("/")
def hello():
	return "<h1 style='color:steelblue'>Hello from NYC CB!!! </h1>"

@app.route("/sarah")
def love():
	return "<h1 style='color:pink;'>I Love you, Sarah June! </h1>"

@app.route("/getSyntheisFromLink", methods=['POST'])
def retrieveModel():
	request_data = request.get_json()
	# data = request_data['data']
	number = request_data['number']
	app.logger.info('Processing get request')
	return {"number": number}

if __name__ == "__main__":
	app.run(host="0.0.0.0",debug=True)
