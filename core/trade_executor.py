# core/trade_executor.py

class TradeExecutor:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def place_order(self, symbol, side, quantity, order_type="market"):
        # Placeholder for actual API call (e.g., Alpaca/Binance)
        print(f"[TRADE] {side.upper()} {quantity} shares of {symbol} ({order_type} order)")
        return {"status": "success", "order_id": "SIMULATED_ORDER_123"}

# core/trade_executor.py

class TradingStrategy:
    def generate_signal(self, data):
        rsi = self.market_analyzer.calculate_rsi()
        macd = self.market_analyzer.calculate_macd()
        bb = self.market_analyzer.calculate_bollinger_bands()
        
        if None in [rsi, macd, bb]:
            return None

        latest_rsi = rsi.iloc[-1]
        latest_macd = macd['MACD_12_26_9'].iloc[-1]
        latest_signal = macd['MACDs_12_26_9'].iloc[-1]
        latest_close = data['close'].iloc[-1]
        upper_band = bb['BBU_20_2.0'].iloc[-1]

        # Enhanced logic
        buy_condition = (
            (latest_rsi < 40) and 
            (latest_macd > latest_signal) and 
            (latest_close < upper_band)
        )
        
        sell_condition = (latest_rsi > 60) and (latest_macd < latest_signal)
        
        return "BUY" if buy_condition else "SELL" if sell_condition else "HOLD"