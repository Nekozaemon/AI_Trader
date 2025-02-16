import requests
from textblob import TextBlob
import logging

class NewsAnalyzer:
    def __init__(self):
        self.api_key = "3a35a4219c3e41b8b9ff607f4582ffd8"  # Replace with your key

    def get_sentiment(self, query="forex"):
        """Fetch news and analyze sentiment"""
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.api_key}"
            response = requests.get(url)
            articles = response.json().get("articles", [])
            
            sentiment = 0
            for article in articles:
                analysis = TextBlob(article["title"] + " " + article["description"])
                sentiment += analysis.sentiment.polarity
            
            return sentiment / len(articles) if articles else 0
        except Exception as e:
            logging.error(f"News analysis failed: {e}")
            return 0

