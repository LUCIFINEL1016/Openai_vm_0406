import sys
sys.path.append("/home/hmtf000001/auto_trading_team/venv/lib/python3.11/site-packages")
from dotenv import load_dotenv
import os

class AccountRouter:
    def __init__(self, account_type="DEMO"):
        self.account_type = account_type
        load_dotenv()

    def get_credentials(self):
        if self.account_type == "DEMO":
            return {
                "SIM_IG_USERNAME": os.getenv("SIM_IG_USERNAME"),
                "SIM_IG_PASSWORD": os.getenv("SIM_IG_PASSWORD"),
                "SIM_IG_API_KEY": os.getenv("SIM_IG_API_KEY"),
            }
        else:
            return {
                "LIVE_IG_USERNAME": os.getenv("LIVE_IG_USERNAME"),
                "LIVE_IG_PASSWORD": os.getenv("LIVE_IG_PASSWORD"),
                "LIVE_IG_API_KEY": os.getenv("LIVE_IG_API_KEY"),
            }
