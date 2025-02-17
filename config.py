# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class for AI Trader"""
    
    # MT5 Configuration
    MT5_LOGIN = int(os.getenv('MT5_LOGIN', 0))
    MT5_PASSWORD = os.getenv('MT5_PASSWORD', '')
    MT5_SERVER = os.getenv('MT5_SERVER', '')
    MT5_PATH = r'C:\Program Files\MetaTrader 5\terminal64.exe'
    
    # Trading Parameters
    RISK_PER_TRADE = 0.02  # 2% of account balance
    MAX_LOT_SIZE = 10.0
    SLIPPAGE_PIPS = 3
    MAGIC_NUMBER = 20240801  # Unique bot identifier
    SYMBOLS = ['EURUSD', 'GBPUSD', 'XAUUSD']
    TIMEFRAME = 'M15'
    
    # Path Configuration
    MODEL_DIR = Path('models')
    DATA_DIR = Path('data')
    
    # Telegram Configuration
    TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.MT5_LOGIN:
            raise ValueError("MT5_LOGIN not set in .env")
        if not cls.MT5_PASSWORD:
            raise ValueError("MT5_PASSWORD not set in .env")
        if not cls.MT5_SERVER:
            raise ValueError("MT5_SERVER not set in .env")

# Validate configuration on import
Config.validate()