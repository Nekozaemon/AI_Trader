from flask import Flask, render_template, jsonify
from core.data_handler import DataHandler
from core.market_analyzer import MarketAnalyzer
import threading

app = Flask(__name__)
symbol = "AAPL"

def update_data():
    data = DataHandler(symbol).fetch_live_data()
    analyzer = MarketAnalyzer(data)
    return {
        "rsi": analyzer.calculate_rsi().iloc[-1],
        "macd": analyzer.calculate_macd().iloc[-1].to_dict()
    }

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    return jsonify(update_data())

if __name__ == "__main__":
    threading.Thread(target=app.run).start()