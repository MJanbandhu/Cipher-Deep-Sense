# scripts/model_evaluation.py

from keras.models import load_model
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

def evaluate_model(df):
    """Evaluate the LSTM model."""
    model = load_model('../models/lstm_model.h5')
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['close']])
    
    X, y = [], []
    for i in range(len(df_scaled) - 1):
        X.append(df_scaled[i])
        y.append(df_scaled[i + 1])
    
    X, y = np.array(X), np.array(y)
    y_pred = model.predict(X)
    
    mse = mean_squared_error(y, y_pred)
    print(f"Mean Squared Error: {mse}")

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    evaluate_model(df)