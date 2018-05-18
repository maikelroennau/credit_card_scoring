# Credit Card Scoring - NuBank

Code exercise for Data Scientist position at NuBank.

## Problem statement

One of the most important decisions we make here at Nubank is who we give credit cards to. We want to make sure that we're only
giving credit cards to people who are likely to pay us back.

We have some data from people who we have given a credit card to in the past, and one of our data scientists has created a model
that tries to predict whether someone will pay their credit card bills based on this data.  He claims that the model has really good performance for
this problem, with an AUC score of 0.59 (AUC stands for Area Under the receiver operating characteristic Curve, a common performance metric for classification models) .

We want to start using this model to make approve or decline decisions in real time, but the data scientist has no idea
how to move his research into production.

The data scientist gives you three files:
 - `model.py`: the script which he used to train his model.
 - `training_set.parquet`: the data which he used to train his model.
 - `pip.txt`: the versions of libraries he used in his model

Your task is to create a simple HTTP service that allows us to use this model in production. It should have a POST endpoint
`/predict` which accepts and returns JSON content type payloads. Low latency is an important requirement, as other services will hit this endpoint
whenever data is available for a new possible customer, and will use the predictions that come from your service to make the decision to
send or not a credit card to each customer.

Example input:
```
json
{
    "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
    "score_3": 480.0,
    "score_4": 105.2,
    "score_5": 0.8514,
    "score_6": 94.2,
    "income": 50000
}
```

Example output:
```
json
{
    "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
    "prediction": 0.1495
}
```

Once you're comfortable with your solution, you should try to tackle the issue of retraining: Periodically, once we have
collected some more data, we may want to retrain the model including this extra data. However, we usually need to keep the
old versions working, as they might still be useful. Update your service so that it supports running multiple versions of
the model simultaneously. You can assume that when we want to retrain, a parquet file with the new data will be provided.

We will evaluate your code in a similar way that we usually evaluate code that we send to production, so we expect production
quality code. Pay attention to code organization and make sure it is readable and clean, but also avoid highly
over-engineered solutions. Try to be succinct and functional with your configuration and setup code.
As a general guideline, a good solution can be implemented with less than 1000 lines of code, including setup and documentation.

You should deliver a git repository with your code and a short README file outlining the solution and explaining how to
build and run the code (preferably you should provide scripts to deploy and start the service),
we just ask that you keep your repository private (GitLab and BitBucket offer free private repositories).

Feel free to ask any questions during the process, but also try make your own assumptions and document them in the
submission, which is an important part of the development.

Good luck!
