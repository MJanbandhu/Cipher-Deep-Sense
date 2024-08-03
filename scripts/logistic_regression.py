# scripts/logistic_regression.py

from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def train_logistic_regression(df):
    """Train a Logistic Regression model."""
    X = df[['open', 'high', 'low', 'volume']]
    y = df['close'] > df['open']  # Binary classification: price increase or not
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=0)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Logistic Regression Accuracy: {accuracy}")

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    train_logistic_regression(df)