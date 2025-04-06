import unittest
from simulated_execution import place_trade, hedging_trade, calculate_daily_pnl

class TestExecutionModule(unittest.TestCase):
    def test_place_trade(self):
        result = place_trade("AAPL", "BUY", 10, 150.0)
        self.assertEqual(result['asset'], "AAPL")
        self.assertEqual(result['direction'], "BUY")
        self.assertEqual(result['quantity'], 10)
        self.assertEqual(result['entry_price'], 150.0)

    def test_hedging_trade(self):
        hedge_position = hedging_trade(100, {"price": 200})
        self.assertEqual(hedge_position, -50)

    def test_calculate_daily_pnl(self):
        pnl = calculate_daily_pnl()
        self.assertIsInstance(pnl, float)

if __name__ == "__main__":
    unittest.main()
