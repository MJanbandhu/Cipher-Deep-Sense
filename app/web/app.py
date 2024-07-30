# app/web/app.py

from flask import Flask, render_template, request
import pandas as pd
from keras.models import load_model
from scripts.time_series_forecasting import time_series_forecast
from scripts.ann_model import train_ann
from scripts.logistic_regression import train_logistic_regression
from scripts.decision_tree import train_decision_tree
from scripts.random_forest import train_random_forest
from scripts.svm_model import train_svm

app = Flask(__name__)

# Load models
ann_model = load_model('../models/ann_model.h5')
# Add other model loading if needed

@app.route('/')
def index():
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    
    # Get predictions
    forecast_20s = time_series_forecast(df, steps=1)  # Change as needed
    forecast_3m = time_series_forecast(df, steps=3*60)  # Change as needed
    
    # Historical data
    recent_data = df.tail(60)  # Last 60 seconds of data
    
    return render_template('index.html', forecast_20s=forecast_20s, forecast_3m=forecast_3m, recent_data=recent_data)

if __name__ == "__main__":
    app.run(debug=True)