
import unittest

class TestSimulatedTrading(unittest.TestCase):
    def test_simulated_order_execution(self):
        sample_order = {'id': 1, 'symbol': 'BTC/USD', 'quantity': 0.01, 'price': 60000, 'type': 'BUY'}
        response = execute_trade(sample_order)
        self.assertIsNotNone(response, "Trade execution failed.")
        self.assertIn("status", response, "Response missing status field.")
        self.assertEqual(response["status"], "FILLED", "Order was not filled.")

if __name__ == '__main__':
    unittest.main()
