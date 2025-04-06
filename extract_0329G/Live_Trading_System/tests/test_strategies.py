import unittest
from strategies import MovingAverageStrategy
from unittest.mock import patch

class TestMovingAverageStrategy(unittest.TestCase):
    @patch('strategies.MovingAverageStrategy.get_historical_data')
    def test_generate_signal(self, mock_get_historical_data):
        """Test signal generation using the moving average strategy."""
        # Mock historical data
        mock_get_historical_data.return_value = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
        
        # Initialize the strategy instance
        strategy = MovingAverageStrategy(short_window=3, long_window=5)
        signal = strategy.generate_signal('AAPL')

        # Assert that the generated signal is 'BUY'
        self.assertEqual(signal, 'BUY')

if __name__ == '__main__':
    unittest.main()