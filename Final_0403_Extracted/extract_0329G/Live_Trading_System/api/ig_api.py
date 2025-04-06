import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys from environment variables
IG_API_KEY = os.getenv("IG_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

class IG_API:
    CST = None
    SECURITY_TOKEN = None

    @classmethod
    def authenticate(cls):
        """ Authenticate and get session tokens """
        url = "https://demo-api.ig.com/gateway/deal/session"
        headers = {
            "X-IG-API-KEY": IG_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "VERSION": "3"
        }
        data = {"identifier": IG_USERNAME, "password": IG_PASSWORD}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            cls.CST = response.headers.get("CST")
            cls.SECURITY_TOKEN = response.headers.get("X-SECURITY-TOKEN")
            print("✅ IG API Authentication Successful")
        else:
            print(f"❌ IG API Authentication Failed: {response.status_code}, {response.text}")

    @classmethod
    def fetch_market_data(cls, epic):
        """ Fetch market price data """
        if not cls.CST or not cls.SECURITY_TOKEN:
            cls.authenticate()

        headers = {
            "X-IG-API-KEY": IG_API_KEY,
            "CST": cls.CST,
            "X-SECURITY-TOKEN": cls.SECURITY_TOKEN,
            "Accept": "application/json"
        }
        url = f"https://demo-api.ig.com/gateway/deal/prices/{epic}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

# Test IG API
if __name__ == "__main__":
    IG_API.authenticate()
    data = IG_API.fetch_market_data("CS.D.EURUSD.MINI.IP")
    print(data)