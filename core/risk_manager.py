# core/risk_manager.py

class RiskManager:
    def __init__(self, risk_per_trade=0.02, max_daily_loss=0.05):
        self.risk_per_trade = risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.daily_loss = 0.0

    def calculate_position_size(self, account_balance, trade_risk):
        if account_balance <= 0:
            raise ValueError("Account balance must be > 0.")
        if trade_risk < 0 or trade_risk > 1:
            raise ValueError("Trade risk must be between 0 and 1.")
        return account_balance * self.risk_per_trade * trade_risk

    def update_daily_loss(self, loss):
        if loss < 0:
            raise ValueError("Loss cannot be negative.")
        self.daily_loss += loss
        return self.daily_loss <= self.max_daily_loss

    def reset_daily_loss(self):
        self.daily_loss = 0.0