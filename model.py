import glob
import json
import os
import pickle
from datetime import datetime
from sys import argv

import pandas as pd
from numpy.random import RandomState
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


# Loading configurations
config_file = "config.json"
config = None
with open(config_file, "r") as json_data:
    config = json.loads(json_data.read())


def split_dataset(df, validation_percentage, seed):
    state = RandomState(seed)
    validation_indexes = state.choice(df.index, int(len(df.index) * validation_percentage), replace=False)
    training_set = df.loc[~df.index.isin(validation_indexes)]
    validation_set = df.loc[df.index.isin(validation_indexes)]
    return training_set, validation_set


def save_model(model_data, path=config["model_dir"]):
    # Saving the model with the current date and hour
    filename = "model_{}.sav".format(datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
    pickle.dump(model_data, open(os.path.join(path, filename), "wb"))
    return filename


def load_model(model_name=config["current_model"], path=config["model_dir"]):
    models_list = glob.glob(os.path.join(path, "*.sav"))

    if len(models_list) == 0:
        return None
    elif model_name in models_list:
        return pickle.load(open(model_name, 'rb'))
    else:
        return pickle.load(open(max(models_list, key=os.path.getctime), 'rb'))


def train(data_path=config["dataset_path"]):
    # load the data
    data = pd.read_parquet(data_path)

    # split into training and validation
    training_set, validation_set = split_dataset(data, 0.25, 1)
    print("training set has %s rows" % len(training_set))
    print("validation set has %s rows" % len(validation_set))

    # train model
    training_set["score_3"] = training_set["score_3"].fillna(425)
    training_set["default"] = training_set["default"].fillna(False)
    clf = LogisticRegression(C=0.1)
    clf.fit(training_set[["score_3", "score_4", "score_5", "score_6"]], training_set["default"])

    # evaluate model
    validation_set["score_3"] = validation_set["score_3"].fillna(455)
    validation_set["default"] = validation_set["default"].fillna(False)
    validation_predictions = clf.predict_proba(validation_set[["score_3", "score_4", "score_5", "score_6"]])[:, 1]
    score = roc_auc_score(validation_set[["default"]], validation_predictions)
    print("Model's score: {}".format(score))

    # Saving model to disk, so we can use it later
    model_name = save_model(clf)
    return model_name, score


def predict(model, subject):
    # model: loaded model
    # subject: dict with data to be predicted by the model
    df = pd.DataFrame([subject], columns=subject.keys())
    return round(model.predict_proba(df[["score_3", "score_4", "score_5", "score_6"]])[:, 1][0], 4)


if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == 'train':
            train()
    else:
        pass
