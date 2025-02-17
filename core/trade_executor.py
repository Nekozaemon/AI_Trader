import MetaTrader5 as mt5
import numpy as np
from config import Config
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class MT5TradeExecutor:
    def __init__(self):
        self._initialize_mt5()
        
    def _initialize_mt5(self):
        """Establish MT5 connection with error handling"""
        if not mt5.initialize(login=Config.MT5_LOGIN, 
                            password=Config.MT5_PASSWORD,
                            server=Config.MT5_SERVER,
                            path=Config.MT5_PATH):
            logger.error(f"MT5 initialization failed: {mt5.last_error()}")
            raise ConnectionError("Failed to connect to MT5 terminal")
            
        logger.info(f"Connected to MT5 account {Config.MT5_LOGIN}")

    def execute_trade(self, symbol: str, signal: str, risk: float) -> Optional[Dict]:
        """Execute market order with advanced risk controls"""
        try:
            # Calculate position size
            lot_size = self._calculate_lot_size(symbol, risk)
            if lot_size <= 0:
                return None

            # Prepare order structure
            order_type = mt5.ORDER_TYPE_BUY if signal.lower() == 'buy' else mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "type": order_type,
                "price": price,
                "sl": 0.0,
                "tp": 0.0,
                "deviation": Config.SLIPPAGE_PIPS,
                "magic": Config.MAGIC_NUMBER,
                "comment": "AI Trader",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            
            # Send order
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Order failed: {result.comment}")
                return None
                
            logger.info(f"Executed {symbol} {signal} @ {price} Lots: {lot_size:.2f}")
            return result._asdict()
            
        except Exception as e:
            logger.error(f"Trade execution error: {str(e)}")
            return None

    def _calculate_lot_size(self, symbol: str, risk_percent: float) -> float:
        """Calculate lot size based on account balance and current price"""
        account_info = mt5.account_info()
        if not account_info:
            logger.error("Failed to get account info")
            return 0.0
            
        balance = account_info.balance
        risk_amount = balance * risk_percent
        price = mt5.symbol_info_tick(symbol).ask
        contract_size = mt5.symbol_info(symbol).trade_contract_size
        lot_size = (risk_amount / (price * contract_size))
        
        return min(lot_size, Config.MAX_LOT_SIZE)

    def close_all_positions(self):
        """Close all open positions from this bot"""
        positions = mt5.positions_get(magic=Config.MAGIC_NUMBER)
        for pos in positions:
            close_request = {
                "position": pos.ticket,
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_BUY if pos.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(pos.symbol).ask if pos.type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(pos.symbol).bid,
                "deviation": Config.SLIPPAGE_PIPS,
                "magic": Config.MAGIC_NUMBER,
                "comment": "AI Close",
                "type_time": mt5.ORDER_TIME_GTC,
            }
            mt5.order_send(close_request)