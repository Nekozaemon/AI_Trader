# Trading Configuration
BROKERS = {
    "MyDemo": {
        "login": 90269661,        # MT5 Account Number
        "password": "!tZt0aZi",    # MT5 Password
        "server": "MetaQuotes-Demo"  # From your broker
    }
}

SYMBOLS = ["BTCUSD", "ETHUSD", "XRPUSD"]  # Symbols to trade
TRADE_MODE = "PAPER"  # REAL or PAPER
RISK_PER_TRADE = 0.02  # 2% per trade
MAX_DAILY_LOSS = 0.05  # 5% daily loss limit

# Telegram Configuration
TELEGRAM_TOKEN = "950251170:AAEHwpGH4SKQIG8KgRS6EoHupBX-lZeknlQ"  # From @BotFather
CHAT_ID = "734698844"       # From @userinfobot

# News API
NEWS_API_KEY = "3a35a4219c3e41b8b9ff607f4582ffd8"  # From NewsAPI.org


