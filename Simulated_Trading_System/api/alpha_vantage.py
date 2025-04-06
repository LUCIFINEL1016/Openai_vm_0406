import requests
from api.clients import ALPHA_VANTAGE_API_KEY

# Base URL for Alpha Vantage API
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol):
    """Retrieve stock price from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    try:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        price = data["Time Series (5min)"][latest_time]["1. open"]
        return float(price)
    except KeyError:
        print(f"❌ Alpha Vantage API error: {data}")
        return None