import MetaTrader5 as mt5
import logging
from config import TRADE_MODE, RISK_PER_TRADE, MAX_DAILY_LOSS
from risk_manager import RiskManager
from paper_trading import PaperTrade

risk_manager = RiskManager()
paper_trader = PaperTrade() if TRADE_MODE == "PAPER" else None

def execute_trade(action, symbol):
    try:
        if TRADE_MODE == "REAL":
            if not mt5.initialize():
                raise ConnectionError("MT5 connection failed")
                
            if not risk_manager.can_trade():
                return "Daily loss limit reached"
                
            volume = risk_manager.calculate_position_size(symbol)
            tick = mt5.symbol_info_tick(symbol)
            price = tick.ask if action == "buy" else tick.bid
            sl = price * 0.99 if action == "buy" else price * 1.01
            tp = price * 1.02 if action == "buy" else price * 0.98

            result = mt5.order_send({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 20,
            })
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                risk_manager.update_pnl(result.profit)
                return f"{action} {volume} {symbol} @ {price:.5f}"
            return f"Failed: {result.comment}"
            
        elif TRADE_MODE == "PAPER":
            price = 60000  # Simulated price
            volume = 0.01
            sl = price * 0.99 if action == "buy" else price * 1.01
            tp = price * 1.02 if action == "buy" else price * 0.98
            return paper_trader.execute_trade(action, symbol, price, volume, sl, tp)
            
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if TRADE_MODE == "REAL":
            mt5.shutdown()