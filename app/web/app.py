from flask import Flask, render_template, request, jsonify, send_file
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import os
import matplotlib.pyplot as plt
from keras.models import load_model
from scripts.time_series_forecasting import time_series_forecast
from scripts.ann_model import predict_ann
from scripts.logistic_regression import predict_logistic_regression
from scripts.decision_tree import predict_decision_tree
from scripts.random_forest import predict_random_forest
from scripts.svm_model import predict_svm
from datetime import datetime

app = Flask(__name__)

# Load secret key from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# Set secure cookie settings
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

class ModelPredictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    ann_prediction = db.Column(db.Float, nullable=False)
    logistic_regression_prediction = db.Column(db.Float, nullable=False)
    decision_tree_prediction = db.Column(db.Float, nullable=False)
    random_forest_prediction = db.Column(db.Float, nullable=False)
    svm_prediction = db.Column(db.Float, nullable=False)

class ForecastData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    forecast_5s = db.Column(db.Float, nullable=False)
    forecast_20s = db.Column(db.Float, nullable=False)
    forecast_3m = db.Column(db.Float, nullable=False)

# CSRF protection and rate limiting
csrf = CSRFProtect(app)
limiter = Limiter(app)

def save_chart(df, forecast_5s, forecast_20s, forecast_3m):
    """Save the chart to a file."""
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['value'], label='Real-Time Data', color='black')
    plt.plot(df.index[-len(forecast_5s):], forecast_5s, label='Next 5s Forecast', linestyle='--', color='blue')
    plt.plot(df.index[-len(forecast_20s):], forecast_20s, label='Next 20s Forecast', linestyle='--', color='blue')
    plt.plot(df.index[-len(forecast_3m):], forecast_3m, label='Next 3m Forecast', linestyle='--', color='blue')
    plt.title('Stock Predictions')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('app/web/static/chart.png')  # Save chart as image

def get_color_class(value):
    """Return CSS class based on value."""
    if value < 0:
        return 'negative'
    elif value > 0:
        return 'positive'
    else:
        return 'neutral'

@app.route('/')
def index():
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    
    # Load models
    ann_model = load_model('../models/ann_model.h5')
    logistic_model = load_model('../models/logistic_model.pkl')
    decision_tree_model = load_model('../models/decision_tree_model.pkl')
    random_forest_model = load_model('../models/random_forest_model.pkl')
    svm_model = load_model('../models/svm_model.pkl')

    # Forecast
    forecast_5s = time_series_forecast(df, steps=5)
    forecast_20s = time_series_forecast(df, steps=20)
    forecast_3m = time_series_forecast(df, steps=3*60)
    
    # Predictions
    ann_predictions = predict_ann(df, ann_model)
    logistic_predictions = predict_logistic_regression(df, logistic_model)
    decision_tree_predictions = predict_decision_tree(df, decision_tree_model)
    random_forest_predictions = predict_random_forest(df, random_forest_model)
    svm_predictions = predict_svm(df, svm_model)
    
    # Historical data
    recent_data_10s = df.tail(10)
    recent_data_2m = df.tail(120)

    # Save chart
    save_chart(df, forecast_5s, forecast_20s, forecast_3m)
    
    # Save data to database
    try:
        # Insert stock data
        for index, row in df.iterrows():
            stock_data = StockData(timestamp=row['timestamp'], open=row['open'], high=row['high'],
                                   low=row['low'], close=row['close'], volume=row['volume'])
            db.session.add(stock_data)
        
        # Insert predictions
        prediction_record = ModelPredictions(
            timestamp=datetime.now(),
            ann_prediction=ann_predictions,
            logistic_regression_prediction=logistic_predictions,
            decision_tree_prediction=decision_tree_predictions,
            random_forest_prediction=random_forest_predictions,
            svm_prediction=svm_predictions
        )
        db.session.add(prediction_record)

        # Insert forecast data
        forecast_record = ForecastData(
            timestamp=datetime.now(),
            forecast_5s=forecast_5s,
            forecast_20s=forecast_20s,
            forecast_3m=forecast_3m
        )
        db.session.add(forecast_record)

        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error saving data to the database: {e}")

    return render_template('index.html', 
                           forecast_5s=forecast_5s, 
                           forecast_20s=forecast_20s,
                           forecast_3m=forecast_3m,
                           ann_predictions=ann_predictions,
                           logistic_predictions=logistic_predictions,
                           decision_tree_predictions=decision_tree_predictions,
                           random_forest_predictions=random_forest_predictions,
                           svm_predictions=svm_predictions,
                           recent_data_10s=recent_data_10s,
                           recent_data_2m=recent_data_2m,
                           ann_predictions_past=ann_predictions_past,
                           logistic_predictions_past=logistic_predictions_past,
                           decision_tree_predictions_past=decision_tree_predictions_past,
                           random_forest_predictions_past=random_forest_predictions_past,
                           svm_predictions_past=svm_predictions_past)

@app.route('/api/live-data')
@limiter.limit("5 per minute")
def live_data():
    # Implement fetching live data
    # Example: return static JSON for demonstration
    data = {
        'forecast_5s': 0.1,
        'forecast_20s': 0.2,
        'forecast_3m': 0.3
    }
    return jsonify(data)

@app.route('/api/update-model', methods=['POST'])
@limiter.limit("5 per minute")
def update_model():
    # Implement model updating logic
    return jsonify({'status': 'Model updated successfully'})

@app.route('/chart')
def chart():
    return send_file('app/web/static/chart.png', mimetype='image/png')

if __name__ == "__main__":
    if not os.path.exists('app/web/static'):
        os.makedirs('app/web/static')
    app.run(debug=True)
