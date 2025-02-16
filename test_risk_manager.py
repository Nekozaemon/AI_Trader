# test_risk_manager.py

import unittest
from risk_manager import calculate_position_size, check_daily_loss, RISK_PER_TRADE, MAX_DAILY_LOSS

class TestRiskManager(unittest.TestCase):
    def test_calculate_position_size(self):
        """
        Test the calculate_position_size function.
        """
        # Test normal case
        account_balance = 10000  # Example account balance
        trade_risk = 0.5  # 50% of the risk per trade
        expected_result = account_balance * RISK_PER_TRADE * trade_risk
        actual_result = calculate_position_size(account_balance, trade_risk)
        self.assertEqual(actual_result, expected_result)

        # Test edge case: zero account balance
        with self.assertRaises(ValueError):
            calculate_position_size(0, trade_risk)

        # Test edge case: negative trade risk
        with self.assertRaises(ValueError):
            calculate_position_size(account_balance, -0.1)

        # Test edge case: trade risk greater than 1
        with self.assertRaises(ValueError):
            calculate_position_size(account_balance, 1.1)

    def test_check_daily_loss(self):
        """
        Test the check_daily_loss function.
        """
        # Test normal case: within limit
        daily_loss = 0.04  # 4% loss (within MAX_DAILY_LOSS)
        self.assertTrue(check_daily_loss(daily_loss))

        # Test edge case: exceeds limit
        daily_loss = 0.06  # 6% loss (exceeds MAX_DAILY_LOSS)
        self.assertFalse(check_daily_loss(daily_loss))

        # Test edge case: negative daily loss
        with self.assertRaises(ValueError):
            check_daily_loss(-0.01)

if __name__ == '__main__':
    unittest.main()