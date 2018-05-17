#!/usr/bin/python

#
# Installing required libraries
#
import os
os.system("pip install -r requirements.txt")


#
# Rading config file
#
import json

config_file = "config.json"

if not os.path.isfile(config_file):
    print("Config file not found!")
    print("Setup canceled.")
    exit(1)

json_data = open(config_file).read()
config = json.loads(json_data)


#
# Creating folders and if the dataset file was provided
#
if not os.path.exists(config["model_dir"]):
    print("Creating models directory")
    os.mkdir(config["model_dir"])


if not os.path.exists(config["dataset_path"]):
    print("Dataset not found!")
    print("Setup canceled.")
    exit(1)

#
# Checking for an existing model and adding it to the config file
#
if len(os.listdir(config["model_dir"])) == 0:
    print("Training model")
    os.system("python model.py train")

    # Cheking if model was generated
    if len(os.listdir(config["model_dir"])) == 0:
        print("Model was not found!")
        print("Setup canceled.")
        exit(1)

# Checking trained model (or the most recent one) and addint it to the config file
import glob

list_of_models = glob.glob(os.path.join(config["model_dir"], "*.sav"))
latest_model = max(list_of_models, key=os.path.getctime)

print("Setting model: {}".format(latest_model))
config["current_model"] = latest_model

with open(config_file, 'w') as outfile:
    json.dump(config, outfile)

print("Setup done!")
exit(0)
