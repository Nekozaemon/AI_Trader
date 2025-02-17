# main.py
import os
import time
import schedule
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from dotenv import load_dotenv
import httpx
from core.ml_models import AdaptiveAlphaModel
from core.trade_executor import MT5TradeExecutor
from utils.resource_watchdog import ResourceGuardian
from config import Config
import logging

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize environment
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_report(message: str):
    """Send formatted message to Telegram with error handling"""
    try:
        response = httpx.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
            json={
                "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            },
            timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Telegram notification failed: {str(e)}")

class TradingBot:
    def __init__(self):
        self.model = AdaptiveAlphaModel()
        self.trader = MT5TradeExecutor()
        self.resource_guard = ResourceGuardian()
        self.current_symbol = Config.SYMBOLS[0]
        self.account_info = None
        self.last_trade_report = ""

    def get_mt5_account_status(self) -> str:
        """Fetch and format MT5 account statistics"""
        try:
            self.account_info = mt5.account_info()._asdict()
            positions = mt5.positions_get(magic=Config.MAGIC_NUMBER)
            
            status = (
                f"💼 *Account Overview*\n"
                f"Balance: ${self.account_info['balance']:,.2f}\n"
                f"Equity: ${self.account_info['equity']:,.2f}\n"
                f"Margin Free: ${self.account_info['margin_free']:,.2f}\n"
                f"Open Positions: {len(positions)}"
            )
            return status
        except Exception as e:
            logger.error(f"Account status check failed: {str(e)}")
            return "❌ Failed to fetch account status"

    def execute_trading_cycle(self):
        """Complete trading iteration with enhanced reporting"""
        try:
            # 1. Market Analysis
            rates = mt5.copy_rates_from_pos(
                self.current_symbol, 
                mt5.TIMEFRAME_M15, 
                0, 
                100
            )
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')

            # 2. AI Prediction
            prediction = self.model.predict(df[['open', 'high', 'low', 'close', 'tick_volume']].values)
            
            # 3. Execute Trade
            trade_result = None
            if prediction['signal'] != 'hold':
                trade_result = self.trader.execute_trade(
                    self.current_symbol, 
                    prediction['signal'], 
                    Config.RISK_PER_TRADE
                )

            # 4. Prepare Report
            report = (
                f"📈 *Trading Update* ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n"
                f"🔹 Symbol: {self.current_symbol}\n"
                f"🔹 Signal: {prediction['signal'].upper()}\n"
                f"🔹 Confidence: {prediction['confidence']:.2%}\n"
                f"🔹 Price: {df['close'].iloc[-1]:.5f}\n\n"
                f"{self.get_mt5_account_status()}"
            )
            
            if trade_result:
                report += (
                    f"\n\n✅ *Trade Executed*\n"
                    f"Lots: {trade_result['volume']:.2f}\n"
                    f"Price: {trade_result['price']:.5f}\n"
                    f"ID: {trade_result['order']}"
                )

            # 5. Send Update
            if report != self.last_trade_report:  # Avoid duplicate messages
                send_telegram_report(report)
                self.last_trade_report = report

            # 6. Rotate Symbols
            self._rotate_symbols()

        except Exception as e:
            error_msg = f"🚨 *Trading Error*\n{str(e)[:200]}"
            send_telegram_report(error_msg)
            logger.error(f"Trading cycle failed: {str(e)}")

    def _rotate_symbols(self):
        """Rotate focus between configured symbols"""
        current_index = Config.SYMBOLS.index(self.current_symbol)
        self.current_symbol = Config.SYMBOLS[(current_index + 1) % len(Config.SYMBOLS)]

    def shutdown(self):
        """Graceful shutdown procedure"""
        self.trader.close_all_positions()
        mt5.shutdown()
        send_telegram_report("🔴 Trading Bot Shutdown Complete")
        logger.info("System shutdown successfully")

if __name__ == '__main__':
    bot = TradingBot()
    send_telegram_report("🟢 AI Trading Bot Started Successfully")
    
    # Configure trading schedule
    schedule.every(15).minutes.do(bot.execute_trading_cycle)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        bot.shutdown()
    except Exception as e:
        bot.shutdown()
        raise e