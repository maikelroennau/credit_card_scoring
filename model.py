import pandas as pd
from sklearn.linear_model import LogisticRegression
from numpy.random import RandomState
from sklearn.metrics import roc_auc_score

from constants import *

import os
import pickle
from datetime import datetime


def split_dataset(df, validation_percentage, seed):
    state = RandomState(seed)
    validation_indexes = state.choice(df.index, int(len(df.index) * validation_percentage), replace=False)
    training_set = df.loc[~df.index.isin(validation_indexes)]
    validation_set = df.loc[df.index.isin(validation_indexes)]
    return training_set, validation_set


def save_model(model_data, path=MODELS_PATH):
    # Saving the model with the current date and hour
    filename = "model_{}.sav".format(datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
    pickle.dump(model_data, open(os.path.join(path, filename), "wb"))


def load_model(model_name=CURRENT_MODEL, path=MODELS_PATH):
    return pickle.load(open(os.path.join(path, model_name), 'rb'))


def train(data_path=MODELS_PATH):
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
    print(roc_auc_score(validation_set[["default"]], validation_predictions))

    # Saving model to disk, so we can use it later
    save_model(clf)


def predict(model, subject):
    # model: loaded model
    # subject: dict with data to be predicted by the model 
    df = pd.DataFrame([subject], columns=subject.keys())
    return model.predict_proba(df[["score_3", "score_4", "score_5", "score_6"]])[:, 1][0]


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        if argv[1] == 'train':
            train()
    else:
        pass
