import os
import openai
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Read API Key for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Risk management parameters
MAX_RISK_PER_TRADE = float(os.getenv("MAX_RISK_PER_TRADE", 0.02))  # Maximum risk per trade (2%)
MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", 0.1))  # Maximum total drawdown (10%)

class RiskManagement:
    """Class for handling risk assessment and position sizing."""
    
    def __init__(self, account_balance):
        self.account_balance = account_balance
        self.max_loss_per_trade = self.account_balance * MAX_RISK_PER_TRADE
        self.max_drawdown_limit = self.account_balance * MAX_DRAWDOWN
    
    def assess_risk_level(self, asset, market_data):
        """
        Uses AI to assess the risk level based on market data.
        :param asset: The asset being analyzed.
        :param market_data: Market data as input for risk assessment.
        :return: Risk assessment result (Low Risk / High Risk).
        """
        if not OPENAI_API_KEY:
            print("❌ OpenAI API Key is missing. Cannot assess risk level.")
            return "Unknown Risk"
        
        prompt = f"""
        Analyze the risk level for the following asset based on its market data:
        Asset: {asset}
        Market Data: {market_data}
        Please respond with either "Low Risk" or "High Risk".
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial risk analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"❌ AI risk assessment failed: {e}")
            return "Unknown Risk"
    
    def calculate_position_size(self, entry_price, stop_loss_price):
        """
        Calculates the optimal position size based on risk parameters.
        :param entry_price: The entry price of the trade.
        :param stop_loss_price: The stop-loss price to limit risk.
        :return: The calculated position size.
        """
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit == 0:
            print("⚠️ Stop-loss price is equal to entry price. Risk cannot be calculated.")
            return 0
        position_size = self.max_loss_per_trade / risk_per_unit
        return round(position_size, 2)
    
    def check_risk_violation(self, total_loss):
        """
        Checks if the total loss exceeds the maximum drawdown limit.
        :param total_loss: The current total loss in the account.
        :return: True if within risk limits, False if exceeded.
        """
        if total_loss >= self.max_drawdown_limit:
            print("⚠️ Maximum drawdown limit reached. Trading should be paused.")
            return False
        return True