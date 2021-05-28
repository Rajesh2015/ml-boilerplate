import os
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import requests
import logging
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root_response():
    """Info."""
    response = make_response("ML-Boilerplate API. Endpoints: /api/v1.0/test, /api/v1.0/predict")
    return response


@app.route('/api/v1.0/test', methods=['GET'])
def test_response():
    """Return a sample JSON response."""
    sample_response = {
        "items": [
            { "id": 1, "name": "Apples",  "price": "$2" },
            { "id": 2, "name": "Peaches", "price": "$5" }
        ]
    }
    response = make_response(jsonify(sample_response))
    return response

@app.route('/api/v1.0/predict', methods=['POST', 'OPTIONS'])
def predict_response():
    """Execute a prediction."""
    try:
        data = json.dumps(request.json)
        headers = {'Content-type': 'application/json'}
        app.logger.info('req: ' + data)

        # sample_response = ["Henry Williams: My name is Henry Williams.", "What is your name? ", "1.0"]
        # response = make_response(jsonify(sample_response))

        # url = 'https://an-development-eu-west-1.cloud.databricks.com/model/ConvEngine7/5/invocations'
        # post_response = requests.post(
        #     url, 
        #     data=data, 
        #     headers=headers,
        #     auth=('token', 'dapi5c1d3cabdbbadb0720e9cb7691772650'))

        # url = 'http://192.168.0.11:5000/invocations'
        url = os.environ.get('MLFLOW_ENDPOINT')
        app.logger.info('url: ' + url)
        post_response = requests.post(url, data=data, headers=headers)

        app.logger.info(post_response)
        response = make_response(jsonify(str(post_response.status_code) + ' ' + str(post_response.content)))

    except Exception as exc:
        app.logger.error(exc)
        response = make_response(jsonify('Error calling model engine: ' + str(exc)))
    except:
        app.logger.error('Unknown exception')

    # app.logger.info(response)
    return response