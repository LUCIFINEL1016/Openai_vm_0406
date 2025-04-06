
import sys
import os

# 強制添加 Trading_System 到 sys.path，確保可以導入 api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Simulated_Trading_System")))

from market_data import fetch_market_data
import unittest

class TestMarketData(unittest.TestCase):
    def test_fetch_valid_asset(self):
        data = fetch_market_data("AAPL")
        self.assertIsNotNone(data)

    def test_fetch_invalid_asset(self):
        data = fetch_market_data("INVALID_SYMBOL")
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
