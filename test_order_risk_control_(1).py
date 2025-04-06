
import requests
import json
import time
from datetime import datetime

API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"
ORDER_SIZE = 0.2
STOP_DISTANCE = 10
LIMIT_DISTANCE = 20

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
        cst = res.headers.get("CST")
        xst = res.headers.get("X-SECURITY-TOKEN")
        print("✅ 登入成功")
        return cst, xst
    else:
        print("❌ 登入失敗", res.status_code, res.text)
        return None, None

def get_account_funds(cst, xst):
    url = "https://api.ig.com/gateway/deal/accounts"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        accounts = res.json()["accounts"]
        for acc in accounts:
            if acc["accountId"] == ACCOUNT_ID:
                balance = float(acc["balance"]["available"])
                print(f"💰 可用資金為：{balance:.2f}")
                return balance
        print("⚠ 找不到符合的帳戶 ID")
    else:
        print("❌ 無法取得帳戶資訊")
    return None

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
    else:
        print("❌ 無法獲取最小下單單位", res.status_code)
        return None

def place_order(epic, direction, size, stop_distance, limit_distance, cst, xst):
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
        "limitDistance": limit_distance,
        "stopDistance": stop_distance,
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        deal_ref = res.json().get("dealReference")
        print(f"✅ 下單成功 | 代碼: {deal_ref}")
        return deal_ref
    else:
        print("❌ 下單失敗：", res.status_code, res.text)
        return None

def run_test():
    print("📌 開始單品測試")
    cst, xst = login()
    if not cst or not xst:
        return

    funds = get_account_funds(cst, xst)
    if funds is None:
        print("🚫 無法取得資金，取消下單")
        return

    min_size = get_min_deal_size(PRODUCT_EPIC, cst, xst)
    if min_size is None:
        print("🚫 無法取得下單限制")
        return

    if ORDER_SIZE < min_size:
        print(f"⚠️ 倉位小於最小下單單位（{min_size}），請調整")
        return

    # *此處可加上 margin 檢查邏輯（略）

    place_order(PRODUCT_EPIC, "BUY", ORDER_SIZE, STOP_DISTANCE, LIMIT_DISTANCE, cst, xst)

if __name__ == "__main__":
    run_test()
