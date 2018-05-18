#!/usr/bin/python

import json
import os

from flask import Flask, request

from model import load_model, predict, train


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def get_prediction():
    input_json = request.json

    # Getting a prediction for inputed data
    prediction = predict(current_model, input_json)

    # Building JSON response
    response = {}
    response["id"] = input_json["id"]
    response["prediction"] = prediction

    return json.dumps(response)


@app.route("/train", methods=["POST"])
def train_model():
    input_json = request.json

    if not os.path.exists(input_json["dataset_path"]):
        return str({})

    model_name, score = train(input_json["dataset_path"])

    # Building JSON response
    response = {}
    response["model_name"] = model_name
    response["score"] = score

    return json.dumps(response)


@app.route("/update_model", methods=["POST"])
def update_model():
    global current_model

    input_json = request.json

    current_model = load_model(model_name=input_json["model_name"])

    # Loading config file to be updated with new model
    config = load_config(config_file)
    config["current_model"] = input_json["model_name"]

    with open(config_file, "w") as outfile:
        json.dump(config, outfile)

    # Building JSON response
    response = {}
    response["current_model"] = config["current_model"]

    return json.dumps(response)


@app.route("/config", methods=["GET"])
def get_config():
    return json.dumps(load_config(config_file))


def load_config(config_path):
    # Loading config file from disk
    with open(config_path, "r") as json_data:
        config = json.loads(json_data.read())
        return config


if __name__ == "__main__":
    config_file = "config.json"
    current_model = load_model()

    if current_model is None:
        print("No model was found.")
        print("Stopping execution")
        exit(1)

    app.run(port=8080)
