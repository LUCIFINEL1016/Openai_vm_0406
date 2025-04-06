from Live_Trading_System.AutoOrder_LogCapture import log_order_result


import logging
from time import sleep
from binance.client import Client
from ig_api import IG_API

class TradeExecution:
    def __init__(self, binance_api_key, binance_secret_key, ig_api_key):
        self.binance_client = Client(binance_api_key, binance_secret_key)
        self.ig_client = IG_API(ig_api_key)
        self.logger = logging.getLogger("TradeExecution")
        logging.basicConfig(filename="logs/trade_execution.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def execute_trade(self, platform, symbol, side, quantity, price=None):
        """ 在指定平台執行交易（買/賣）"""
        self.logger.info(f"Initiating {side.upper()} order: {symbol} | Qty: {quantity} | Price: {price if price else 'Market'}")

        try:
            if platform.lower() == "binance":
                order = self._execute_binance_trade(symbol, side, quantity, price)
            elif platform.lower() == "ig":
                order = self._execute_ig_trade(symbol, side, quantity, price)
            else:
                raise ValueError("Unsupported platform")

            if order:
                self.logger.info(f"Trade Executed: {order}")
                return order
            else:
                self.logger.error("Trade execution failed!")
                return None
        except Exception as e:
            self.logger.error(f"Trade execution error: {e}")
            return None

    def _execute_binance_trade(self, symbol, side, quantity, price=None):
        """ Binance 交易執行 """
        order_type = "LIMIT" if price else "MARKET"
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type,
            "quantity": quantity,
            "price": price if price else None
        }

        try:
            order = self.binance_client.create_order(**params)
            self.logger.info(f"Binance Order: {order}")
            sleep(2)  # 避免 API 限制
            return order
        except Exception as e:
            self.logger.error(f"Binance trade error: {e}")
            return None

    def _execute_ig_trade(self, symbol, side, quantity, price=None):
        """ IG Market 交易執行 """
        try:
            order = self.ig_client.execute_order(symbol, side, quantity, price)
            self.logger.info(f"IG Market Order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"IG Market trade error: {e}")
            return None
