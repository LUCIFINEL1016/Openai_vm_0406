import unittest
import subprocess
import os

class TestSimulatedTrading(unittest.TestCase):
    def test_run_simulated_trading(self):
        """Test if the simulated trading system runs correctly."""
        test_script = os.path.join(os.getcwd(), "..", "simulated_trading_system", "simulated_trading.py")
        result = subprocess.run(["python", test_script], capture_output=True, text=True)
        
        self.assertIn("📊 Today's P&L:", result.stdout)  # Check if P&L output is present
        self.assertNotIn("❌", result.stdout)  # Ensure there are no error messages

if __name__ == "__main__":
    unittest.main()