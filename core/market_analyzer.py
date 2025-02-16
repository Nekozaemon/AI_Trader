# core/market_analyzer.py

import pandas as pd
import pandas_ta as ta

class MarketAnalyzer:
    def __init__(self, data):
        self.data = data

    def calculate_rsi(self, period=14):
        try:
            if 'close' not in self.data.columns:
                raise ValueError("Missing 'close' column.")
            return ta.rsi(self.data['close'], length=period)
        except Exception as e:
            print(f"RSI Error: {e}")
            return None

    def calculate_macd(self, fast=12, slow=26, signal=9):
        try:
            if 'close' not in self.data.columns:
                raise ValueError("Missing 'close' column.")
            macd = ta.macd(self.data['close'], fast=fast, slow=slow, signal=signal)
            return macd
        except Exception as e:
            print(f"MACD Error: {e}")
            return None