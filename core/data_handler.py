# core/data_handler.py

import pandas as pd
import yfinance as yf

class DataHandler:
    def __init__(self, symbol, period="1d", interval="5m"):
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def fetch_live_data(self):
        try:
            data = yf.download(
                self.symbol, 
                period=self.period, 
                interval=self.interval,
                progress=False
            )
            if data.empty:
                return pd.DataFrame()
            
            # Flatten MultiIndex columns and remove symbol suffix
            if isinstance(data.columns, pd.MultiIndex):
                # Keep only the primary column name (e.g., "Close" instead of "Close_AAPL")
                data.columns = [col[0].lower() for col in data.columns]
            else:
                data.columns = [col.lower() for col in data.columns]
            
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()