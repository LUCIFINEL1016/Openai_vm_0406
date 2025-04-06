
import requests
import json
from Live_Trading_System.utils.ig_auth import get_ig_headers
from Live_Trading_System.utils.epic_lookup import get_epic
from Live_Trading_System.AutoOrder_LogCapture import log_order_result

def place_eurusd_order(account_id, epic="CS.D.EURUSD.CFD.IP", direction="BUY", size=1.0, stop_level=1.0720, limit_level=1.0805):
    headers, ig_url = get_ig_headers()
    url = f"{ig_url}/gateway/deal/positions/otc"
    payload = {
        "epic": epic,
        "expiry": "-",
        "direction": direction,
        "size": str(size),
        "orderType": "MARKET",
        "timeInForce": "FILL_OR_KILL",
        "guaranteedStop": False,
        "stopLevel": stop_level,
        "limitLevel": limit_level,
        "forceOpen": True,
        "currencyCode": "USD",
        "dealReference": "AUTO_EURUSD_TEST"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    log_order_result(stop_level, size, result, symbol="EURUSD")
    return result

def fallback_eurusd_order(price, quantity):
    print(f"💶 觸發 EUR/USD Fallback 掛單邏輯 @ {price}，數量：{quantity}")
    return place_eurusd_order(account_id="QL5HA", size=quantity, stop_level=1.0720, limit_level=1.0805)
