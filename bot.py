# bot.py (Final Version)

import os
import logging
import httpx
import warnings
import pandas as pd
from core.risk_manager import RiskManager
from core.market_analyzer import MarketAnalyzer
from core.data_handler import DataHandler
from core.ml_models import MLModels
from core.news_handler import get_news
from utils.logger import setup_logger

# Configuration
warnings.filterwarnings("ignore")
logger = setup_logger()

# Telegram Settings (REPLACE THESE!)
TELEGRAM_BOT_TOKEN = "950251170:AAEHwpGH4SKQIG8KgRS6EoHupBX-lZeknlQ"
TELEGRAM_CHAT_ID = "734698844"

def send_telegram_message(rsi, macd, predictions, news):
    """Send professional trading report to Telegram"""
    try:
        # Format message with Markdown
        report = (
            "📊 *AI Trader Report*\n"
            "══════════════════\n"
            f"🕒 *Timestamp*: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            "📉 *Technical Analysis*\n"
            f"- RSI: `{rsi:.2f}` {'(Oversold ⚠️)' if rsi < 30 else '(Overbought ⚠️)' if rsi > 70 else '(Neutral)'}\n"
            f"- MACD: `{macd:.4f}` {'↑ Bullish' if macd > 0 else '↓ Bearish'}\n\n"
            
            "🔮 *Price Predictions (Next 10 Periods)*\n" + 
            "\n".join([f"{i+1}. ${price:.2f}" for i, price in enumerate(predictions)]) + "\n\n"
            
            "📰 *Market News*\n" + 
            "\n".join([f"• {headline.strip()}" for headline in news.split("|")[:3]]) + "\n\n"
            "⚠️ *Predictions are algorithmic - verify before trading*"
        )

        # Send message
        response = httpx.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": report,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )
        response.raise_for_status()
        logger.info("Telegram report sent successfully")
        
    except Exception as e:
        logger.error(f"Failed to send Telegram report: {str(e)}")

def main():
    """Main trading execution flow"""
    logger.info("Initializing AI Trader...")
    
    try:
        # Initialize modules
        symbol = "AAPL"
        data_handler = DataHandler(symbol, period="7d", interval="5m")
        market_data = data_handler.fetch_live_data()
        
        if market_data.empty:
            logger.error("Failed to fetch market data")
            return

        logger.info(f"Latest market data:\n{market_data.tail()}")

        # Technical indicators
        analyzer = MarketAnalyzer(market_data)
        rsi_value = analyzer.calculate_rsi().iloc[-1]
        macd_value = analyzer.calculate_macd()['MACD_12_26_9'].iloc[-1]
        
        logger.info(f"RSI: {rsi_value:.2f}, MACD: {macd_value:.4f}")

        # Machine Learning predictions
        ml_engine = MLModels(market_data)
        model = ml_engine.train_model()
        predictions = ml_engine.predict_future(model, steps=10).flatten()
        logger.info(f"Generated predictions: {predictions}")

        # News analysis
        news_text = get_news() or "No relevant news found"
        logger.info(f"News headlines: {news_text[:100]}...")

        # Send comprehensive report
        send_telegram_message(
            rsi=rsi_value,
            macd=macd_value,
            predictions=predictions,
            news=news_text
        )

        logger.info("AI Trader cycle completed successfully")

    except Exception as e:
        logger.error(f"Critical failure: {str(e)}")
        send_telegram_message(
            rsi=0,
            macd=0,
            predictions=[],
            news=f"❌ System Error: {str(e)[:200]}"
        )

if __name__ == "__main__":
    main()