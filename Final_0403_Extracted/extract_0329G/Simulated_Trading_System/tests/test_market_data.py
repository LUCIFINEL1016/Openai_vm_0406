import unittest
from simulated_trading_system.market_data import fetch_market_data

class TestMarketData(unittest.TestCase):
    def test_fetch_valid_asset(self):
        """Test fetching valid market data."""
        asset = "AAPL"
        data = fetch_market_data(asset)
        self.assertIsNotNone(data)
        self.assertIn("bid", data)  # Assuming the API response includes a "bid" price
    
    def test_fetch_invalid_asset(self):
        """Test fetching data with an invalid asset code."""
        asset = "INVALID_ASSET"
        data = fetch_market_data(asset)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()