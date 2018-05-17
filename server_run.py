#!/usr/bin/python

import json
from flask import Flask, request

from model import load_model, predict, train


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def get_prediction():
    input_json = request.json

    # Getting a prediction for inputed data
    prediction = predict(curent_model, input_json)

    # Building JSON response
    response = {}
    response["id"] = input_json["id"]
    response["prediction"] = prediction

    return str(response)


@app.route('/train', methods=['POST'])
def train_model():
    input_json = request.json

    model_name, score = train(input_json["dataset_path"])

    # Building JSON response
    response = {}
    response["model_name"] = model_name
    response["score"] = score

    return str(response)


@app.route('/update_model', methods=['POST'])
def update_model():
    import os

    input_json = request.json

    curent_model = load_model(input_json["model_name"])

    # Loading config file to be updated with new model
    json_data = open(config_file).read()
    config = json.loads(json_data)
    config["current_model"] = os.path.join(config["model_dir"], input_json["model_name"])

    with open(config_file, 'w') as outfile:
        json.dump(config, outfile)

    # Building JSON response
    response = {}
    response["current_model"] = config["current_model"]

    return str(response)


@app.route('/config', methods=['GET'])
def get_config():
    # Loadin config file and sending it back
    json_data = open(config_file).read()
    config = json.loads(json_data)

    return str(config)


if __name__ == '__main__':
    config_file = "config.json"
    curent_model = load_model()

    app.run(port='8080')
