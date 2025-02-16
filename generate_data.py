import pandas as pd
import numpy as np

# Generate fake BTCUSD data
dates = pd.date_range(start="2024-01-01", periods=1000, freq="T")
prices = np.random.normal(loc=60000, scale=500, size=1000).cumsum()

df = pd.DataFrame({
    "time": dates,
    "open": prices,
    "high": prices + 200,
    "low": prices - 200,
    "close": prices + 50,
    "volume": np.random.randint(500, 1500, 1000)
})

df.to_csv("BTCUSD_historical.csv", index=False)
print("Fake data generated!")