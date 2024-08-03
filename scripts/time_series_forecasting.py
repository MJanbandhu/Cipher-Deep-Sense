# scripts/time_series_forecasting.py

import pandas as pd
from statsmodels.tsa.forecast import ForecastResults
from statsmodels.tsa.arima_model import ARIMA

def time_series_forecast(df, steps=20):
    """Forecast stock prices using ARIMA."""
    model = ARIMA(df['close'], order=(5,1,0))
    model_fit = model.fit(disp=0)
    forecast = model_fit.forecast(steps=steps)[0]
    return forecast

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    forecast = time_series_forecast(df, steps=20)
    print(f"Forecast for next 20 seconds: {forecast}")