# main.py
import os
import httpx
import pandas as pd
from dotenv import load_dotenv
from core.risk_manager import RiskManager
from core.market_analyzer import MarketAnalyzer
from core.data_handler import DataHandler
from core.ml_models import MLModels
from core.news_handler import get_news
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

# Get credentials from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_report(rsi, macd, predictions, news):
    """Send comprehensive trading report to Telegram with news"""
    try:
        # Format predictions
        pred_list = "\n".join([f"• Period {i+1}: ${p:.2f}" for i, p in enumerate(predictions)])
        
        # Format news
        news_items = "\n".join([f"📰 {item}" for item in news[:3]]) if news else "No significant news"

        message = (
            f"📈 *AI Trader Report*\n\n"
            f"🔹 *RSI*: {rsi:.2f}\n"
            f"🔹 *MACD*: {macd:.4f}\n\n"
            f"📊 *Price Predictions*\n{pred_list}\n\n"
            f"📮 *Market News*\n{news_items}\n\n"
            "⚠️ *Algorithmic predictions - verify before trading*"
        )

        response = httpx.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )
        response.raise_for_status()
        logger.info("Telegram report sent successfully")
        
    except Exception as e:
        logger.error(f"Telegram error: {str(e)}")

def main():
    logger.info("Starting AI Trader...")
    
    try:
        symbol = "AAPL"
        
        # Data handling
        data_handler = DataHandler(symbol, period="7d", interval="5m")
        market_data = data_handler.fetch_live_data()
        
        if market_data.empty:
            logger.error("Failed to fetch market data")
            return

        # Technical analysis
        analyzer = MarketAnalyzer(market_data)
        rsi = analyzer.calculate_rsi().iloc[-1]
        macd = analyzer.calculate_macd()['MACD_12_26_9'].iloc[-1]
        
        # ML predictions
        ml_model = MLModels(market_data)
        model = ml_model.train_model()
        predictions = ml_model.predict_future(model, steps=10).flatten()
        
        # News analysis
        news = get_news()
        
        # Send comprehensive report
        send_telegram_report(rsi, macd, predictions, news)
        
        logger.info("AI Trader cycle completed successfully")

    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        send_telegram_report(0, 0, [], [f"System Error: {str(e)[:200]}"])  # Error notification

if __name__ == "__main__":
    main()