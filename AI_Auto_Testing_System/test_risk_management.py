
import sys
import os

# 確保可以找到 AI_Auto_Testing_System
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from risk_management import RiskManagement
import unittest

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManagement(max_loss_per_trade=0.02, volatility_threshold=0.05)

    def test_calculate_position_size(self):
        position_size = self.risk_manager.calculate_position_size(10000, 0.02)
        self.assertEqual(position_size, 200)

    def test_check_risk(self):
        result = self.risk_manager.check_risk(100, 95, 10000)
        self.assertTrue(result)

    def test_check_market_volatility(self):
        volatility_ok = self.risk_manager.check_market_volatility([100, 102, 98, 101])
        self.assertTrue(volatility_ok)

if __name__ == "__main__":
    unittest.main()
