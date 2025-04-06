
import requests
import json
from datetime import datetime

# === IG 認證資訊 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# === 測試標的清單 ===
PRODUCTS = [
    {"epic": "CS.D.EURUSD.CFD.IP", "name": "EUR/USD", "direction": "BUY"},
    {"epic": "CS.D.NATGAS.CFD.IP", "name": "NATGAS", "direction": "SELL"},
    {"epic": "IX.D.NASDAQ.IFD.IP", "name": "NASDAQ", "direction": "SELL"},
]

# 登入取得 CST、X-SECURITY-TOKEN
def login():
    url = "https://api.ig.com/gateway/deal/session"
    payload = {"identifier": USERNAME, "password": PASSWORD}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("✅ 登入成功")
        return response.headers.get("CST"), response.headers.get("X-SECURITY-TOKEN")
    else:
        print("❌ 登入失敗")
        return None, None

# 查詢帳戶資金
def get_account_funds(cst, xst):
    url = f"https://api.ig.com/gateway/deal/accounts"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        accounts = res.json()["accounts"]
        for acc in accounts:
            if acc["accountId"] == ACCOUNT_ID:
                return float(acc.get("balance", {}).get("available", 0))
    return 0.0

# 查詢商品最小下單單位
def get_min_deal_size(epic, cst, xst):
    url = f"https://api.ig.com/gateway/deal/markets/{epic}"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return float(res.json()["dealingRules"]["minDealSize"]["value"])
    return 0.1

# 送出市價單（含風控）
def place_order(epic, direction, size, cst, xst):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    payload = {
        "epic": epic,
        "expiry": "-",
        "direction": direction,
        "size": size,
        "orderType": "MARKET",
        "guaranteedStop": False,
        "forceOpen": True,
        "limitDistance": 20,
        "stopDistance": 10,
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        deal_ref = res.json().get("dealReference")
        print(f"✅ 下單成功：{epic} | 倉位: {size} | 方向: {direction} | 參考碼: {deal_ref}")
        return deal_ref
    else:
        print(f"❌ 下單失敗（{epic}）: {res.status_code} - {res.text}")
        return None

# 主程式
def run():
    print("📌 開始 EUR/USD 單筆測試")
    cst, xst = login()
    if not cst or not xst:
        return
    available = get_account_funds(cst, xst)
    print(f"💰 可用資金: {available:.2f}")

    for p in PRODUCTS:
        epic = p["epic"]
        direction = p["direction"]
        min_size = get_min_deal_size(epic, cst, xst)
        print(f"🔍 商品 {p['name']} 最小倉位：{min_size}")
        if available < 50:
            print("⚠️ 資金過低，跳過下單")
            continue
        place_order(epic, direction, min_size, cst, xst)
        break  # 單筆測試只下第一個成功的產品

if __name__ == "__main__":
    run()
