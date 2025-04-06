
import requests
import json
import time
from datetime import datetime

# === 認證資料 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"
ORDER_SIZE = 0.2

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# === 登入 IG ===
def login():
    url = "https://api.ig.com/gateway/deal/session"
    payload = {
        "identifier": USERNAME,
        "password": PASSWORD
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code == 200:
        print("✅ 登入成功")
        cst = res.headers.get("CST")
        xst = res.headers.get("X-SECURITY-TOKEN")
        return cst, xst
    else:
        print("❌ 登入失敗", res.status_code, res.text)
        return None, None

# === 查詢可用資金 ===
def get_available_funds(cst, xst):
    url = f"https://api.ig.com/gateway/deal/accounts"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        accounts = res.json()["accounts"]
        for acc in accounts:
            if acc["accountId"] == ACCOUNT_ID:
                return float(acc.get("availableCash", 0))
    return None

# === 查詢最小下單量 ===
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

# === 下單功能 ===
def place_order(epic, size, direction, cst, xst):
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
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID,
        "limitDistance": 20,
        "stopDistance": 10
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        deal_ref = res.json().get("dealReference", "")
        return deal_ref
    else:
        print("❌ 下單請求失敗:", res.status_code, res.text)
        return None

# === 查詢交易是否成功 ===
def confirm_order(deal_ref, cst, xst):
    url = f"https://api.ig.com/gateway/deal/confirm/{deal_ref}"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    headers["Accept"] = "application/json"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        status = data.get("dealStatus")
        reason = data.get("reason")
        if status == "ACCEPTED":
            print(f"✅ 交易確認成功：{status}")
        else:
            print(f"🚫 交易被拒：{reason}")
    else:
        print("❌ 查詢訂單失敗", res.status_code, res.text)

# === 主測試流程 ===
def run_test():
    print("📌 開始單品測試")
    cst, xst = login()
    if not cst or not xst:
        return

    funds = get_available_funds(cst, xst)
    if funds is None:
        print("⚠️ 無法查詢資金")
        return
    print(f"✅ 可用資金：{funds:.2f}")

    min_size = get_min_deal_size(PRODUCT_EPIC, cst, xst)
    if min_size is None:
        print("⚠️ 無法查詢最小下單量")
        return
    print(f"✅ 最小倉位：{min_size}")

    if ORDER_SIZE < min_size:
        print(f"⚠️ 下單量低於最小需求（{min_size}），請調整")
        return

    deal_ref = place_order(PRODUCT_EPIC, ORDER_SIZE, "BUY", cst, xst)
    if deal_ref:
        print(f"📨 送出訂單，參考碼：{deal_ref}")
        time.sleep(2)
        confirm_order(deal_ref, cst, xst)

if __name__ == "__main__":
    run_test()
