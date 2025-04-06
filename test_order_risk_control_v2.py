
import requests
import json
from datetime import datetime

API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

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
        print("✅ 登入成功")
        return cst, xst
    else:
        print("❌ 登入失敗：", response.status_code, response.text)
        return None, None

def get_account_funds(cst, xst):
    url = f"https://api.ig.com/gateway/deal/accounts"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        accounts = response.json()["accounts"]
        for acc in accounts:
            if acc["accountId"] == ACCOUNT_ID:
                balance = float(acc["balance"]["available"])
                return balance
        print("⚠ 找不到指定帳戶資訊")
        return None
    else:
        print("❌ 無法取得帳戶資金：", response.status_code, response.text)
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
        "limitDistance": 20,
        "stopDistance": 10,
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        deal_ref = response.json().get("dealReference", "")
        print(f"✅ 下單成功！參考碼: {deal_ref}")
        return deal_ref
    else:
        print("❌ 下單失敗：", response.status_code, response.text)
        return None

def run_test():
    print("📌 開始單品測試")
    cst, xst = login()
    if not cst or not xst:
        return

    funds = get_account_funds(cst, xst)
    if funds is None:
        print("🚫 無法獲取可用資金")
        return

    min_size = get_min_deal_size(PRODUCT_EPIC, cst, xst)
    if min_size is None:
        return

    print(f"✅ 可用資金：{funds:.2f}")
    print(f"📏 最小倉位：{min_size}")

    test_size = min_size
    est_risk = test_size * 10  # 模擬每單風險

    if funds < est_risk:
        print(f"🚫 資金不足以承擔風險（需求：約 {est_risk:.2f} USD）")
        return

    place_order(PRODUCT_EPIC, test_size, "BUY", cst, xst)

if __name__ == "__main__":
    run_test()
