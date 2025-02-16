import MetaTrader5 as mt5
import pandas as pd

def collect_crypto_data():
    """Fetch historical data for crypto pairs"""
    if not mt5.initialize():
        print("Failed to connect to MT5")
        return
    
    # Fetch BTCUSD data
    try:
        print("Fetching BTCUSD data...")
        btc_data = mt5.copy_rates_from_pos("BTCUSD", mt5.TIMEFRAME_M1, 0, 1000)
        if btc_data is None:
            print("No data received for BTCUSD. Check symbol availability.")
            return
        
        df = pd.DataFrame(btc_data)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.to_csv("BTCUSD_historical.csv", index=False)
        print("Saved BTCUSD_historical.csv with", len(df), "rows")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    collect_crypto_data()