import unittest
from unittest.mock import patch
from Trading_System.Simulated_Trading_System.simulated_execution import execute_trade
from utility import TradeLog

class TestExecution(unittest.TestCase):
    @patch('execution.TradeLog')
    def test_execute_trade_buy(self, MockTradeLog):
        """Test executing a BUY trade."""
        # Mock trade log
        mock_trade_log = MockTradeLog.return_value
        
        # Test buy operation
        asset = 'AAPL'
        direction = 'BUY'
        quantity = 10
        price = 150.0
        
        # Execute trade
        result = execute_trade(asset, direction, quantity, price)
        
        # Assert trade was successful
        self.assertTrue(result)
        mock_trade_log.record_trade.assert_called_once_with(asset, direction, quantity, price)

    @patch('execution.TradeLog')
    def test_execute_trade_sell(self, MockTradeLog):
        """Test executing a SELL trade."""
        # Mock trade log
        mock_trade_log = MockTradeLog.return_value
        
        # Test sell operation
        asset = 'AAPL'
        direction = 'SELL'
        quantity = 5
        price = 155.0
        
        # Execute trade
        result = execute_trade(asset, direction, quantity, price)
        
        # Assert trade was successful
        self.assertTrue(result)
        mock_trade_log.record_trade.assert_called_once_with(asset, direction, quantity, price)

    @patch('execution.TradeLog')
    def test_execute_trade_invalid_direction(self, MockTradeLog):
        """Test executing a trade with an invalid direction."""
        # Invalid trade direction
        asset = 'AAPL'
        direction = 'HOLD'  # Invalid direction
        quantity = 5
        price = 155.0
        
        # Execute trade, expected to fail
        result = execute_trade(asset, direction, quantity, price)
        
        # Assert trade was unsuccessful
        self.assertFalse(result)
        MockTradeLog.return_value.record_trade.assert_not_called()

if __name__ == '__main__':
    unittest.main()