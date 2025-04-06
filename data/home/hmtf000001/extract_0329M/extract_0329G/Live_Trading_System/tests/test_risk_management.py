import unittest
from risk_management import RiskManagement

class TestRiskManagement(unittest.TestCase):
    def test_calculate_position_size(self):
        """Test position size calculation based on risk management."""
        # Initialize the risk management instance
        risk_management = RiskManagement(account_balance=10000, risk_per_trade=0.01)
        
        # Calculate position size
        position_size = risk_management.calculate_position_size(stop_loss=50)
        
        # Assert that the position size is correct
        self.assertEqual(position_size, 2)

if __name__ == '__main__':
    unittest.main()