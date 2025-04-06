from binance.client import Client
from api.clients import BINANCE_API_KEY, BINANCE_SECRET_KEY

# Initialize Binance client
binance_client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

def get_binance_price(symbol):
    """Retrieve the latest price of a given cryptocurrency from Binance."""
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        print(f"❌ Binance API error: {e}")
        return None