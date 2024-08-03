# scripts/svm_model.py

from sklearn.svm import SVR
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_svm(df):
    """Train a Support Vector Machine model."""
    X = df[['open', 'high', 'low', 'volume']]
    y = df['close']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    model = SVR(kernel='rbf')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    print(f"SVM Mean Squared Error: {mse}")

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    train_svm(df)