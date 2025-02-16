import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import logging

class AITrader:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200)

    def train(self, data_path):
        df = pd.read_csv(data_path)
        df['returns'] = df['close'].pct_change()
        df['sma_20'] = df['close'].rolling(20).mean()
        df['rsi'] = self._calculate_rsi(df['close'])
        df.dropna(inplace=True)

        X = df[['returns', 'sma_20', 'rsi']]
        y = np.where(df['returns'].shift(-1) > 0, 1, 0)
        
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        logging.info(f"Trained model with {len(X_train)} samples")

    def _calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        return 100 - (100 / (1 + (avg_gain / avg_loss)))

    def predict(self, data, sentiment=0):
        prediction = self.model.predict(data)
        if sentiment > 0.2:
            return "buy"
        elif sentiment < -0.2:
            return "sell"
        return "buy" if prediction == 1 else "sell"