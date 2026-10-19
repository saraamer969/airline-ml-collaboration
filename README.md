@"
# Airline Passenger Satisfaction Prediction

A machine learning web application that predicts whether an airline passenger is likely to be satisfied or neutral/dissatisfied.

## Features

- Random Forest classification model
- Data preprocessing and model evaluation
- Feature importance visualizations
- Flask REST API for predictions
- Angular frontend with a passenger input form
- Prediction probabilities displayed in the interface

## Technologies

- Python, pandas, NumPy, scikit-learn
- Flask and Flask-CORS
- Angular, TypeScript, HTML, CSS
- Git and GitHub

## Project Structure

- rf_airline.py: trains and evaluates the Random Forest model
- backend/app.py: Flask prediction API
- test_api.py: API testing script
- airline-frontend/: Angular frontend
- train.csv: local training dataset
- requirements.txt: Python dependencies
- .gitignore: files excluded from Git

## Setup

### 1. Install Python dependencies

From the project root:

```bash
pip install -r requirements.txt