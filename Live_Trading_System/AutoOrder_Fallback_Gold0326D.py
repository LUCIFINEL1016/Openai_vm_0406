# AutoOrder_Fallback_Gold0326D.py - Rebuilt version
import requests
import json
from Live_Trading_System.utils.ig_auth import get_ig_headers
from Live_Trading_System.utils.epic_lookup import get_epic

def place_gold_order(account_id, epic="CS.D.CFDGOLD.CFDGC.IP", direction="BUY", size=0.3, stop_level=3018, limit_level=3035):
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
        "dealReference": "AUTO_GOLD_TEST"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    log_order_result(price, size, result, symbol='GOLD')
    return result
# Live_Trading_System/AutoOrder_Fallback_Gold0326D.py

from Live_Trading_System.AutoOrder_LogCapture import log_order_result

def fallback_gold_order(price, quantity):
    print(f"🪙 觸發 GOLD Fallback 掛單邏輯 @ {price}，數量：{quantity}")
    # 尚未連接真實下單，僅模擬輸出
