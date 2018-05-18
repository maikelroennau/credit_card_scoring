#!/usr/bin/python

import glob
import json
import os
import subprocess as sp
import time

import requests


def test_predict():
    print("\n###")
    print("Testing prediction")

    server = start_server()

    try:
        data = {"id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0", "score_3": 480.0, "score_4": 105.2, "score_5": 0.8514, "score_6": 94.2, "income": 500000}

        response = requests.post("http://localhost:8080/predict", json=data)
        response = str(response.text)

        print("RESPONSE: {}".format(response))

        if response == '{"id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0", "prediction": 0.1495}':
            print("\nPredict endpoint: PASS")
            print("###")
            stop_server(server)
            exit(0)
        else:
            print("\nPredict endpoint: FAIL")
            print("###")            
            stop_server(server)
            exit(1)
    except:
        stop_server(server)


def test_train_model():
    print("\n###")
    print("Testing train model")

    server = start_server()

    try:
        config = load_config(config_file)
        n_models = len(os.listdir(config["model_dir"]))

        data = {"dataset_path": "training_set.parquet"}
        requests.post("http://localhost:8080/train", json=data)

        if n_models + 1 == len(os.listdir(config["model_dir"])):
            print("\nTrain endpoint: PASS")
            print("###")
            stop_server(server)
            exit(0)
        else:
            print("\nTrain endpoint: FAIL")
            print("###")            
            stop_server(server)
            exit(1)
    except:
        stop_server(server)


def test_update_model():
    print("\n###")
    print("Testing update model")

    server = start_server()

    old_model = load_config(config_file)["current_model"]

    # Using the same file
    data = {"dataset_path": "training_set.parquet"}
    response = requests.post("http://localhost:8080/train", json=data)

    # For some reason the response is coming with single quotes and that is not a proper JSON
    # So I need this ugly implementation to work around this...
    model_name = json.loads(response.text.replace("'", "\""))["model_name"]

    data = {"model_name": "{}".format(model_name)}
    response = requests.post("http://localhost:8080/update_model", json=data)

    model_name = json.loads(response.text.replace("'", "\""))["current_model"]

    if old_model != model_name:
        print("\nUpdate model endpoint: PASS")
        print("###")
        stop_server(server)
        exit(0)
    else:
        print("\nUpdate model endpoint: FAIL")
        print("###")        
        stop_server(server)
        exit(1)

    try:
        pass
    except:
        stop_server(server)


def test_config():
    print("\n###")
    print("Testing config")

    server = start_server()

    try:
        config = load_config(config_file)
        response = requests.get("http://localhost:8080/config")

        if json.dumps(config) == response.text:
            print("\nConfig endpoint: PASS")
            print("###")
            stop_server(server)
            exit(0)
        else:
            print("\nConfig endpoint: FAIL")
            print("###")            
            stop_server(server)
            exit(1)
    except:
        stop_server(server)


def start_server():
    server = sp.Popen(['python', 'server_run.py'])

    # Giving a few seconds to have the server start
    time.sleep(3)

    return server


def stop_server(server_process):
    sp.Popen.terminate(server_process)


def load_config(config_path):
    # Loading config file from disk
    with open(config_path, "r") as json_data:
        config = json.loads(json_data.read())
        return config


if __name__ == "__main__":
    config_file = "config.json"

    # Tests to run
    test_config()
    test_predict()
    test_train_model()
    test_update_model()
