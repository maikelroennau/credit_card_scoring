#!/usr/bin/python

from flask import Flask, request
# from flask.ext.jsonpify import jsonify
# from flask_restful import Api, Resource
# from sqlalchemy import create_engine

from model import load_model, predict


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def get_prediction():
    input_json = request.json

    # Getting a prediction for inputed data
    prediction = predict(model, input_json)

    # Building JSON response
    response = {}
    response["id"] = input_json["id"]
    response["prediction"] = prediction

    return str(response)


if __name__ == '__main__':
    model = load_model()

    app.run(port='8091')
