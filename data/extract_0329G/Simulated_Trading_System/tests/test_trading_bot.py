import unittest
from simulated_trading_system.trading_bot import analyze_and_trade

class TestTradingBot(unittest.TestCase):
    def test_analyze_and_trade(self):
        """Test AI trading logic."""
        asset = "AAPL"
        result = analyze_and_trade(asset)
        self.assertIn("BUY", result.upper())  # Assuming AI should return either "BUY" or "SELL"
    
    def test_invalid_asset(self):
        """Test non-existent asset handling."""
        asset = "INVALID_ASSET"
        result = analyze_and_trade(asset)
        self.assertEqual(result, "Error: Asset not found")

if __name__ == '__main__':
    unittest.main()