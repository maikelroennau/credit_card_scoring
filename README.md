# Credit Card Scoring - NuBank

Code exercise for Data Scientist position at NuBank.

## Requirements

See `REQUERIMENTS_READMED.md` for an overview of the development specification.

## How to setup

Note: *The code works both on `Python 2` and `Python 3`, although `Python 2` was used during development and most extensively tested.*

Setting up the system (assumed Linux):
1. Clone the repository
1. Navigate the terminal to the cloned directory
1. Run the setup script: `python setup.py`
    - It will install the requirements
    - Create the models directory 
    - Train the initial model and set it in the `config.json` file
1. Run the tests script: `python run_tests.py`
    - It will test all endpoints services: `/predict`, `/train`, `/update_model`, and `/config`
1. Start the server: `python server_run.py`

## What are the services provided

#### **`/predict`**

This service provides predictions to inputed data.

Example input:
```
{
    "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
    "score_3": 480.0,
    "score_4": 105.2,
    "score_5": 0.8514,
    "score_6": 94.2,
    "income": 50000
}
```

Output:
```
{
    "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
    "prediction": 0.1495
}
```

#### **`/train`**

This service allow the training of a new model given a dataset. To execute a training the server expects to receive the path to the dataset.

Example input:
```
{
    "dataset_path": "training_set.parquet"
}
```

At the end it will returns the score and the model's name:
```
{
    "score": 0.5945,
    "model_name": "model_2018-05-17_21h47m19s.sav"
}
```

To set a newly trained model to be used in further predictions, see the next section.

#### **`/update_model`**

This service allows the current model to be replaced by another one without the need or restarting the server. The server expects to receive the model name (all models should be inside the `trained_models` directory therefore the prefix path is not necessary):

Example input:
```
{
    "model_name": "model_2018-05-17_21h24m06s.sav"
}
```

The server returns the current model name (after updating to the new model) as output, so the modification can be verified:
```
{
    "current_model": "model_2018-05-17_21h24m06s.sav"
}
```
