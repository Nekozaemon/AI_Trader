import MetaTrader5 as mt5
import pandas as pd
import numpy as np
# Example definitions
RISK_PER_TRADE = 0.02  # 2% risk per trade
MAX_DAILY_LOSS = 0.05  # 5% maximum daily loss
class RiskManager:
    def __init__(self):
        self.daily_pnl = 0
        self.trade_count = 0

    def calculate_position_size(self, symbol):
        account_info = mt5.account_info()
        balance = account_info.balance
        tick = mt5.symbol_info_tick(symbol)
        risk_amount = balance * RISK_PER_TRADE
        return round(risk_amount / (tick.ask * 100000), 2)

    def can_trade(self):
        return self.daily_pnl > -(MAX_DAILY_LOSS * mt5.account_info().balance)

    def update_pnl(self, profit):
        self.daily_pnl += profit
        self.trade_count += 1
        # risk_manager.py

# Risk management settings
RISK_PER_TRADE = 0.02  # 2% risk per trade
MAX_DAILY_LOSS = 0.05  # 5% max daily loss

# Function to calculate position size based on risk
def calculate_position_size(account_balance, trade_risk):
    """
    Calculate the position size based on account balance and trade risk.
    
    :param account_balance: Total account balance (float)
    :param trade_risk: Risk percentage for this trade (float)
    :return: Position size (float)
    """
    if account_balance <= 0:
        raise ValueError("Account balance must be greater than 0.")
    if trade_risk < 0 or trade_risk > 1:
        raise ValueError("Trade risk must be between 0 and 1.")
    
    return account_balance * RISK_PER_TRADE * trade_risk

# Function to check if daily loss exceeds the maximum allowed
def check_daily_loss(daily_loss):
    """
    Check if the daily loss exceeds the maximum allowed.
    
    :param daily_loss: Daily loss percentage (float)
    :return: True if within limit, False otherwise
    """
    if daily_loss < 0:
        raise ValueError("Daily loss cannot be negative.")
    
    return daily_loss <= MAX_DAILY_LOSS
import logging

logging.basicConfig(level=logging.INFO)

def calculate_position_size(account_balance, trade_risk):
    logging.info(f"Calculating position size with account balance: {account_balance}, trade risk: {trade_risk}")
    if account_balance <= 0:
        raise ValueError("Account balance must be greater than 0.")
    if trade_risk < 0 or trade_risk > 1:
        raise ValueError("Trade risk must be between 0 and 1.")
    
    position_size = account_balance * RISK_PER_TRADE * trade_risk
    logging.info(f"Position size calculated: {position_size}")
    return position_size