
import requests
import json
import time
from datetime import datetime

# === IG API 資訊 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
EPIC = "CS.D.CFDGOLD.CFDGC.IP"
DIRECTION = "BUY"
CURRENCY = "USD"
STOP_DISTANCE = 10
LIMIT_DISTANCE = 20

# 登入並取得 token
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
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        return r.headers.get("CST"), r.headers.get("X-SECURITY-TOKEN")
    else:
        print("❌ 登入失敗:", r.text)
        return None, None

# 查詢市場是否可交易與最小單位
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
        if data["snapshot"]["marketStatus"] != "TRADEABLE":
            print("🚫 市場目前無法交易")
            return None
        return float(data["dealingRules"]["minDealSize"]["value"])
    else:
        print("❌ 無法取得市場資料")
        return None

# 查詢帳戶資金
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
        for acc in res.json()["accounts"]:
            if acc["accountId"] == ACCOUNT_ID:
                return float(acc["available"]["cash"])
    print("❌ 無法取得帳戶資金")
    return None

# 下單（含風控）
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
        "limitDistance": LIMIT_DISTANCE,
        "stopDistance": STOP_DISTANCE,
        "currencyCode": CURRENCY,
        "accountId": ACCOUNT_ID
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        ref = r.json().get("dealReference")
        print(f"✅ 下單成功 | 代碼: {ref}")
    else:
        print(f"❌ 下單失敗：{r.status_code} - {r.text}")

# 主流程
def run_test():
    print("📌 開始單品測試")
    cst, xst = login()
    if not cst:
        return
    min_size = get_min_deal_size(EPIC, cst, xst)
    if min_size is None:
        return
    funds = get_account_funds(cst, xst)
    if funds is None:
        return
    test_size = min_size
    est_margin = 100  # 粗略假設，實際可透過行情 API 計算
    if funds < est_margin:
        print(f"🚫 資金不足（可用: {funds:.2f}, 需求: {est_margin:.2f}）")
        return
    place_order(EPIC, DIRECTION, test_size, cst, xst)

if __name__ == "__main__":
    run_test()
