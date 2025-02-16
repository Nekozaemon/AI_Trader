import asyncio
from config import TELEGRAM_TOKEN, CHAT_ID
from telegram import Bot

async def send_test_message():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text="✅ Telegram test successful!")
        print("Check Telegram - you should see a message!")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(send_test_message())