from binance.client import Client
import os

class BinanceClient:
    client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))

    @staticmethod
    def get_price(symbol):
        return BinanceClient.client.get_symbol_ticker(symbol=symbol)