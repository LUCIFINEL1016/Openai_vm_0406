import os
import requests
import json
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="logs/trading_live.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# API Credentials
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
IG_API_KEY = os.getenv("IG_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Initialize Binance client
binance_client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# IG Market API class
class IG_API:
    CST = None
    SECURITY_TOKEN = None
    
    @classmethod
    def authenticate(cls):
        """Authenticate and obtain session tokens"""
        url = "https://api.ig.com/gateway/deal/session"
        headers = {
            "X-IG-API-KEY": IG_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": "3"
        }
        data = {"identifier": IG_USERNAME, "password": IG_PASSWORD}
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            cls.CST = response.headers.get("CST")
            cls.SECURITY_TOKEN = response.headers.get("X-SECURITY-TOKEN")
            logging.info("✅ IG API authentication successful.")
        else:
            logging.error(f"❌ IG API authentication failed: {response.text}")
            cls.CST, cls.SECURITY_TOKEN = None, None
    
    @classmethod
    def get_market_data(cls, epic):
        """Fetch market price data from IG API"""
        if not cls.CST or not cls.SECURITY_TOKEN:
            cls.authenticate()
        
        headers = {
            "X-IG-API-KEY": IG_API_KEY,
            "CST": cls.CST,
            "X-SECURITY-TOKEN": cls.SECURITY_TOKEN,
            "Accept": "application/json"
        }
        url = f"https://api.ig.com/gateway/deal/prices/{epic}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"❌ IG API request failed: {e}")
            return None

# Fetch Binance price data
def get_binance_price(symbol):
    """Retrieve the latest price from Binance"""
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        logging.error(f"❌ Binance API error: {e}")
        return None

# Execute a trade
def execute_trade(market, asset, direction, quantity, price):
    """Execute a trade order on Binance or IG Market"""
    if market == "Binance":
        return execute_binance_trade(asset, direction, quantity, price)
    elif market == "IG":
        return execute_ig_trade(asset, direction, quantity)
    else:
        logging.error(f"❌ Invalid market: {market}")
        return None

# Execute Binance trade
def execute_binance_trade(asset, direction, quantity, price):
    """Place a limit order on Binance"""
    try:
        order = binance_client.create_order(
            symbol=asset,
            side=direction,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )
        logging.info(f"✅ Binance Order Executed: {direction} {quantity} {asset} @ {price}")
        return order
    except Exception as e:
        logging.error(f"❌ Binance Trade Execution Failed: {e}")
        return None

# Execute IG Market trade
def execute_ig_trade(asset, direction, quantity):
    """Place a market order on IG Markets"""
    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "CST": IG_API.CST,
        "X-SECURITY-TOKEN": IG_API.SECURITY_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    trade_data = {
        "epic": asset,
        "direction": direction,
        "size": quantity,
        "orderType": "MARKET",
        "currencyCode": "HKD",
        "forceOpen": True
    }
    
    try:
        response = requests.post(
            "https://api.ig.com/gateway/deal/positions/otc",
            json=trade_data,
            headers=headers
        )
        if response.status_code == 200:
            logging.info(f"✅ IG Market Order Executed: {direction} {quantity} {asset}")
            return response.json()
        else:
            logging.error(f"❌ IG Market Trade Failed: {response.text}")
            return None
    except Exception as e:
        logging.error(f"❌ IG Market API Error: {e}")
        return None

# Main Execution
if __name__ == "__main__":
    logging.info("🚀 Starting Live Trading System...")
    IG_API.authenticate()
    
    assets = ["BTCUSDT", "AAPL", "EURUSD"]
    for asset in assets:
        logging.info(f"📊 Processing {asset}...")
        
        if asset in ["BTCUSDT", "ETHUSDT"]:
            price = get_binance_price(asset)
        else:
            price_data = IG_API.get_market_data(asset)
            price = price_data['prices'][0]['closePrice'] if price_data else None
        
        if price:
            execute_trade("Binance", asset, "BUY", 0.01, price)
        else:
            logging.error(f"⚠️ No price data for {asset}, skipping trade.")
def log_transaction(order_id, status, platform_response):
    logging.info(f"Order {order_id}: Status: {status}, Response: {platform_response}")

import logging

# 設置日誌配置
logging.basicConfig(filename='logs/trading.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_transaction(order_id, status, platform_response):
    log_message = f"Order {order_id}: Status: {status}, Response: {platform_response}"
    logging.info(log_message)

import logging
import os

# 確保日誌目錄存在
log_dir = os.path.join(os.path.dirname(__file__), '../Logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 設置日誌配置
log_file = os.path.join(log_dir, 'trading.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_transaction(order_id, status, platform_response):
    log_message = f"Order {order_id}: Status: {status}, Response: {platform_response}"
    logging.info(log_message)
