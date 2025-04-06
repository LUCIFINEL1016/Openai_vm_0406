import os
from dotenv import load_dotenv

# Load `.env` file
load_dotenv()

# ✅ Trading System Configuration
TOTAL_CAPITAL_HKD = 200000  # Total available capital in HKD
BINANCE_CAPITAL_HKD = 100000  # Capital allocated for Binance trading
IG_MARKET_CAPITAL_HKD = 100000  # Capital allocated for IG Market trading
LEVERAGE = 2  # Available leverage options: 1x, 2x, 5x

# ✅ Risk Management Settings
MAX_RISK_PER_TRADE = 0.02  # Maximum risk per trade: 2%
MAX_DRAW_DOWN = 0.1  # Maximum total asset drawdown: 10%