import pandas as pd
import numpy as np

class PaperTrade:
    def __init__(self):
        self.balance = 10000
        self.positions = {}
        self.trade_history = []

    def execute_trade(self, action, symbol, price, volume, sl=None, tp=None):
        trade = {
            "timestamp": pd.Timestamp.now(),
            "symbol": symbol,
            "action": action,
            "price": price,
            "volume": volume,
            "sl": sl,
            "tp": tp
        }
        self.trade_history.append(trade)
        
        if action == "buy":
            self.positions[symbol] = trade
            return f"📝 Paper BUY {symbol} {volume} @ {price:.5f} | SL: {sl:.2f} TP: {tp:.2f}"
        else:
            if symbol in self.positions:
                closed_trade = self.positions.pop(symbol)
                profit = (price - closed_trade["price"]) * volume
                self.balance += profit
                return f"📝 Paper SELL {symbol} {volume} @ {price:.5f} | PNL: {profit:.2f}"
            return "No position to close"