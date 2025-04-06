
import requests
import json
from Live_Trading_System.utils.ig_auth import get_ig_headers
from Live_Trading_System.utils.epic_lookup import get_epic
from Live_Trading_System.AutoOrder_LogCapture import log_order_result

def place_oil_order(account_id, epic="CL.D.CRM2024.CFD.IP", direction="BUY", size=0.5, stop_level=6907.3, limit_level=7107.3):
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
        "dealReference": "AUTO_OIL_TEST"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    log_order_result(stop_level, size, result, symbol="USOIL")
    return result

def fallback_oil_order(price, quantity):
    print(f"🛢️ 觸發 USOIL Fallback 掛單邏輯 @ {price}，數量：{quantity}")
    return place_oil_order(account_id="QL5HA", size=quantity, stop_level=6907.3, limit_level=7107.3)
