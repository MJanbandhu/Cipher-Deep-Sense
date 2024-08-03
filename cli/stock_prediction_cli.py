# cli/stock_prediction_cli.py

import argparse
import pandas as pd
from keras.models import load_model
from scripts.time_series_forecasting import time_series_forecast
from scripts.ann_model import predict_ann
from scripts.logistic_regression import predict_logistic_regression
from scripts.decision_tree import predict_decision_tree
from scripts.random_forest import predict_random_forest
from scripts.svm_model import predict_svm
import matplotlib.pyplot as plt

def print_colored(text, color):
    """Print text with the specified color."""
    colors = {'red': '\033[91m', 'blue': '\033[94m', 'white': '\033[97m', 'reset': '\033[0m'}
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def plot_chart(df, forecast_5s, forecast_20s, forecast_3m):
    """Plot the forecast and real-time data."""
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
    plt.show()

def format_prediction(prediction):
    """Format the prediction with color coding."""
    if prediction < 0:
        return print_colored(f"{prediction}", 'red')
    elif prediction > 0:
        return print_colored(f"{prediction}", 'blue')
    else:
        return print_colored(f"{prediction}", 'white')

def main():
    parser = argparse.ArgumentParser(description='Stock Prediction Command-Line Interface')
    parser.add_argument('--data', type=str, default='../data/processed/stock_data_features.csv', help='Path to the stock data CSV file')
    args = parser.parse_args()

    # Load models
    ann_model = load_model('../models/ann_model.h5')
    logistic_model = load_model('../models/logistic_model.pkl')
    decision_tree_model = load_model('../models/decision_tree_model.pkl')
    random_forest_model = load_model('../models/random_forest_model.pkl')
    svm_model = load_model('../models/svm_model.pkl')

    # Load data
    df = pd.read_csv(args.data)
    
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
    
    # Print the results in a structured format
    print("\n--- Forecasts ---")
    format_prediction(f"Next 5 Seconds: {forecast_5s}")
    format_prediction(f"Next 20 Seconds: {forecast_20s}")
    format_prediction(f"Next 3 Minutes: {forecast_3m}")
    
    print("\n--- Model Predictions ---")
    format_prediction(f"ANN: {ann_predictions}")
    format_prediction(f"Logistic Regression: {logistic_predictions}")
    format_prediction(f"Decision Tree: {decision_tree_predictions}")
    format_prediction(f"Random Forest: {random_forest_predictions}")
    format_prediction(f"SVM: {svm_predictions}")
    
    print("\n--- Historical Data ---")
    print("Last 10 Seconds Data:")
    print(recent_data_10s)
    print("\nLast 2 Minutes Data:")
    print(recent_data_2m)

    # Plot the chart
    plot_chart(df, forecast_5s, forecast_20s, forecast_3m)

if __name__ == "__main__":
    main()
