import requests
import os

class AlphaVantage:
    @staticmethod
    def get_market_data(symbol):
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&apikey={api_key}"
        return requests.get(url).json()