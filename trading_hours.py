from datetime import datetime, time

class TradingHours:
    def __init__(self):
        self.london_open = time(8, 0)   # 8 AM GMT
        self.new_york_close = time(22, 0)  # 10 PM GMT
    
    def should_trade(self):
        """Check if current time is within trading hours"""
        now = datetime.utcnow().time()
        return self.london_open <= now <= self.new_york_close