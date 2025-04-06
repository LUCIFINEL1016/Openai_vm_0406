import unittest
from simulated_trading_system.trading_bot import TradingStrategy

class TestTradingBot(unittest.TestCase):
    def test_analyze_trade(self):
        """Test AI trading strategy."""
        strategy = TradingStrategy()
        test_market_data = {"price": 150, "trend": "up"}
        result = strategy.analyze_and_trade("AAPL", test_market_data)

        # Ensure AI returns a trade direction (either "BUY" or "SELL")
        self.assertTrue("BUY" in result.upper() or "SELL" in result.upper())  

if __name__ == "__main__":
    unittest.main()
import unittest

class TestRiskManagement(unittest.TestCase):
    def test_risk_parameters(self):
        self.assertGreaterEqual(MAX_RISK_PERCENT, 0.01, "Risk percentage too low.")
        self.assertLessEqual(MAX_RISK_PERCENT, 0.05, "Risk percentage too high.")

if __name__ == '__main__':
    unittest.main()
