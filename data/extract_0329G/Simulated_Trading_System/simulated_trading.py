import os
import sys
import openai
import re
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import functions from the simulated_execution module
from simulated_execution import place_trade, hedging_trade, calculate_daily_pnl
from risk_management import RiskManagement

# Set up logging
LOG_FILE = "logs/simulated_trading.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load environment variables
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
env_path = os.path.join(os.getcwd(), "Simulated_Trading_System", ".env")
load_dotenv(env_path)

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# IG Market asset code mapping
IG_ASSET_MAP = {
    "XAU": "CS.D.USAGC.SPOT",
    "XAG": "CS.D.USAUS.SPOT",
    "WTI": "CC.D.CL.USS.IP",
    "NG": "CC.D.NG.USS.IP",
    "CORN": "CC.D.CCORN.USS.IP",
    "EURUSD": "CS.D.EURUSD.MINI.IP",
    "USDJPY": "CS.D.USDJPY.MINI.IP",
    "AAPL": "IX.D.AAPL.CASH.IP",
    "TSLA": "IX.D.TSLA.CASH.IP",
}

class IG_API:
    """Handles IG API authentication and token management."""
    CST = None
    SECURITY_TOKEN = None

    @classmethod
    def refresh_tokens(cls):
        """Refresh IG API authentication tokens."""
        url = "https://demo-api.ig.com/gateway/deal/session"
        headers = {
            "X-IG-API-KEY": os.getenv("IG_API_KEY"),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "VERSION": "3",
        }
        data = {
            "identifier": os.getenv("IG_USERNAME"),
            "password": os.getenv("IG_PASSWORD"),
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            cls.CST = response.headers.get("CST")
            cls.SECURITY_TOKEN = response.headers.get("X-SECURITY-TOKEN")
            logging.info("✅ IG API Token successfully refreshed!")
        else:
            logging.error(f"❌ IG API Error: {response.json()}")
            cls.CST, cls.SECURITY_TOKEN = None, None

IG_API.refresh_tokens()

def analyze_and_trade(asset):
    """AI analyzes market data and executes trading decisions."""
    logging.info(f"Analyzing asset: {asset}")

    try:
        market_data = fetch_market_data(asset)
        if not market_data:
            logging.warning(f"No market data for {asset}, skipping...")
            return

        # Sentiment Analysis
        sentiment = analyze_sentiment(asset)
        logging.info(f"Market Sentiment for {asset}: {sentiment}")

        # Risk Assessment
        risk_manager = RiskManagement(account_balance=SIMULATED_BALANCE)
        risk_level = risk_manager.assess_risk_level(asset, market_data)
        logging.info(f"Risk Level for {asset}: {risk_level}")

        # AI-Driven Trading Decision
        prompt = f"""
        Analyze trading for {asset}:
        - Market Sentiment: {sentiment}
        - Risk Level: {risk_level}
        - Market Data: {market_data}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial trading assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        recommendation = response.choices[0].message.content
        logging.info(f"AI Recommendation for {asset}: {recommendation}")

        # Extract Trading Parameters
        entry_price_match = re.search(r"Entry Price:\s*(\d+\.?\d*)", recommendation)
        if not entry_price_match:
            logging.error(f"❌ Failed to extract entry price for {asset}")
            return
        entry_price = float(entry_price_match.group(1))
        direction = "BUY" if "Long" in recommendation else "SELL"

        # Dynamic Position Sizing Strategy
        allocation = 0.1 if risk_level == "Low Risk" else 0.05
        trade_size = round(SIMULATED_BALANCE * LEVERAGE * allocation / entry_price, 2)

        # Apply Hedging Strategy if Enabled
        if HEDGING_ENABLED:
            hedge_direction = "SELL" if direction == "BUY" else "BUY"
            hedging_trade(asset, hedge_direction, trade_size)

        # Execute Trade
        place_trade(asset, direction, trade_size, entry_price)
        logging.info(f"✅ Trade executed for {asset}: {direction} {trade_size} units at {entry_price}")

    except Exception as e:
        logging.error(f"❌ Error in trading execution for {asset}: {e}")

if __name__ == "__main__":
    logging.info("Starting simulated trading system...")
    start_time = time.time()

    for asset in IG_ASSET_MAP:
        analyze_and_trade(asset)

    calculate_daily_pnl()
    execution_time = round(time.time() - start_time, 2)
    logging.info(f"⏱️ Execution time: {execution_time} seconds")

