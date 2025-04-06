
import requests
import json
import time
from datetime import datetime

# IG API credentials
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# List of products to trade (can be expanded)
PRODUCTS = [
    {"epic": "CS.D.CFDGOLD.CFDGC.IP", "name": "GOLD", "direction": "BUY"},
    {"epic": "CS.D.NATGAS.CFD.IP", "name": "NATGAS", "direction": "SELL"},
    {"epic": "IX.D.NASDAQ.IFD.IP", "name": "NASDAQ", "direction": "BUY"},
    {"epic": "CS.D.USDJPY.CFD.IP", "name": "USDJPY", "direction": "SELL"},
    {"epic": "CS.D.AAPL.CFD.IP", "name": "AAPL", "direction": "BUY"}
]

# Check if the market is open (weekdays from 9:00 AM to 5:00 PM)
def is_market_open():
    now = datetime.now()
    weekday = now.weekday()  # 0-6: Monday-Sunday
    market_open_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    market_close_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
    
    # Check if today is a weekday and within the market open time
    if 0 <= weekday <= 4 and market_open_time <= now <= market_close_time:
        return True
    else:
        print("❌ It's either a non-trading day or outside of trading hours!")
        return False

# Login to IG API and return CST and X-SECURITY-TOKEN
def login():
    url = "https://api.ig.com/gateway/deal/session"
    payload = {
        "identifier": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        cst = response.headers.get("CST")
        xst = response.headers.get("X-SECURITY-TOKEN")
        print("✅ Login successful")
        return cst, xst
    else:
        print("❌ Login failed:", response.status_code)
        return None, None

# Place market order (including stop loss and take profit)
def place_order(epic, direction, cst, xst):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst

    payload = {
        "epic": epic,
        "expiry": "-",  # CFD account
        "direction": direction,
        "size": 0.2,  # Small size
        "orderType": "MARKET",
        "guaranteedStop": False,
        "forceOpen": True,
        "level": None,
        "limitDistance": 20,  # Take profit distance
        "stopDistance": 10,   # Stop loss distance
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        deal_ref = response.json().get("dealReference", "")
        print(f"✅ {epic} Order placed successfully | Direction: {direction} | Reference: {deal_ref}")
        return deal_ref
    else:
        print(f"❌ Order failed ({epic}): {response.status_code} - {response.text}")
        return None

# Check if the product can be traded (market status and streaming available)
def is_product_tradeable(epic, cst, xst):
    url = f"https://api.ig.com/gateway/deal/markets/{epic}"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False, "Query failed"
    
    data = res.json()
    min_size = float(data["dealingRules"]["minDealSize"]["value"])
    market_status = data["snapshot"]["marketStatus"]
    stream_available = data["snapshot"]["streamingPricesAvailable"]
    
    if market_status != "TRADEABLE" or not stream_available:
        return False, "Not tradable or no pricing available"
    
    return True, min_size

# Main execution
def run():
    print(f"📌 Starting automated trading task: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if market is open
    if not is_market_open():
        return

    # Login to IG and get CST and X-SECURITY-TOKEN
    cst, xst = login()
    if not cst or not xst:
        return

    # Loop through products and place orders
    for p in PRODUCTS:
        ok, min_size = is_product_tradeable(p["epic"], cst, xst)
        if not ok:
            print(f"🚫 Cannot trade {p['name']} due to: {min_size}")
            continue

        size = max(0.2, min_size)
        place_order(p["epic"], p["direction"], cst, xst)

# Run the program
if __name__ == "__main__":
    run()
