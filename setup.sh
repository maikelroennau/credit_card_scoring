#!/bin/bash

# pip install -r requirements.txt

DIRECTORY="trained_models"
PORT=8080

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

if [ "$(ls -A $DIRECTORY)" ]; then
    echo "No model found."
    echo "Training model..."

    python model.py train
fi

echo "Starting server" 
python http_server.py 8080