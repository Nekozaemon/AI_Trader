# core/news_handler.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_news():
    """Fetch financial news using NewsAPI"""
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "category": "business",
                "language": "en",
                "apiKey": os.getenv("NEWSAPI_KEY")
            }
        )
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return [article['title'] for article in articles[:3]]  # Return top 3 headlines
        
    except Exception as e:
        print(f"News API error: {str(e)}")
        return None