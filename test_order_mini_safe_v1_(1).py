
import requests
import json
from datetime import datetime
import time

# === 認證資料 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"

# === 測試標的（可改為其他產品）===
PRODUCT = {
    "epic": "CS.D.USDJPY.CFD.IP",  # 外匯 USD/JPY
    "name": "USDJPY",
    "direction": "BUY"
}

# === 登入 IG ===
def login():
    url = "https://api.ig.com/gateway/deal/session"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "identifier": USERNAME,
        "password": PASSWORD
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        return res.headers["CST"], res.headers["X-SECURITY-TOKEN"]
    else:
        print("登入失敗：", res.status_code, res.text)
        return None, None

# === 查詢資金 ===
def get_funds(cst, xst):
    url = "https://api.ig.com/gateway/deal/accounts"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        for acc in data["accounts"]:
            if acc["accountId"] == ACCOUNT_ID:
                return float(acc.get("balance", {}).get("available", 0.0))
    return None

# === 查詢產品下單條件 ===
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
        data = res.json()
        return float(data["dealingRules"]["minDealSize"]["value"])
    return None

# === 下單 ===
def place_order(epic, direction, size, cst, xst):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Content-Type": "application/json",
        "Version": "2"
    }
    payload = {
        "epic": epic,
        "expiry": "-",
        "direction": direction,
        "size": size,
        "orderType": "MARKET",
        "guaranteedStop": False,
        "forceOpen": True,
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID,
        "stopDistance": 10,
        "limitDistance": 20
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        deal_ref = res.json().get("dealReference", "")
        print(f"✅ 成功送出下單，參考碼：{deal_ref}")
        return deal_ref
    else:
        print("❌ 下單失敗：", res.status_code, res.text)
        return None

# === 主程序 ===
def run_test():
    print("📌 啟動 Mini Forex 下單測試")
    cst, xst = login()
    if not cst:
        return
    funds = get_funds(cst, xst)
    if funds is None:
        print("⚠️ 無法查詢資金")
        return
    print(f"✅ 可用資金：{funds}")

    min_size = get_min_deal_size(PRODUCT["epic"], cst, xst)
    if not min_size:
        print("⚠️ 查詢最小倉位失敗")
        return
    print(f"✅ 最小倉位：{min_size}")

    # 設定測試倉位
    size = max(min_size, 0.5)
    if funds < 10:  # 若可用資金太少
        print("🚫 資金過低，取消送單")
        return

    # 嘗試下單
    place_order(PRODUCT["epic"], PRODUCT["direction"], size, cst, xst)

if __name__ == "__main__":
    run_test()
