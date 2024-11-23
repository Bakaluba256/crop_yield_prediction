# Yield Prediction Application

## Overview

This application predicts crop yield based on user inputs such as area, crop type, year, rainfall, pesticide usage, and temperature. It consists of:

- **Backend**: A Flask API to serve predictions.
- **Frontend**: An interactive HTML interface.
- **Model**: A RandomForestRegressor trained on the provided dataset.

## Usage

### 1. Train the Model

Run `model_train.py` to preprocess the dataset, train the model, and save it.

### 2. Run the Flask API

Execute `app.py` to start the API. It listens on `http://127.0.0.1:5000`.

### 3. Open the Frontend

Load `index.html` in a browser. Enter the required inputs and view the predicted yield.

## Files

- **model_train.py**: Trains the model.
- **app.py**: Backend API.
- **index.html**: Frontend.
- **styles.css**: Frontend.

## Dependencies

- Python libraries: Flask, scikit-learn, joblib, pandas, numpy.
