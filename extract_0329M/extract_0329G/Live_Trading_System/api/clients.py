import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    IG_API_KEY = os.getenv("IG_API_KEY")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")