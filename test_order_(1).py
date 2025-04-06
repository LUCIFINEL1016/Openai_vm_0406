
import requests
import json
from datetime import datetime

# === 基本設定 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
TEST_EPIC = "CS.D.CFDGOLD.CFDGC.IP"
DIRECTION = "BUY"
SIZE = 0.1  # 測試用小額倉位
STOP_DISTANCE = 10
LIMIT_DISTANCE = 20

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
    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code == 200:
        cst = res.headers.get("CST")
        xst = res.headers.get("X-SECURITY-TOKEN")
        print("✅ 登入成功")
        return cst, xst
    else:
        print("❌ 登入失敗", res.status_code, res.text)
        return None, None

def get_min_deal_size(epic, cst, xst):
    url = f"https://api.ig.com/gateway/deal/markets/{epic}"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        min_size = float(data["dealingRules"]["minDealSize"]["value"])
        return min_size
    else:
        print("❌ 無法獲取最小下單單位", res.status_code)
        return None

def place_order(epic, direction, size, stop_distance, limit_distance, cst, xst):
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
        "limitDistance": limit_distance,
        "stopDistance": stop_distance,
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        print(f"✅ 下單成功：{epic}")
    else:
        print(f"❌ 下單失敗：{res.status_code}", res.text)

# === 主程式測試流程 ===
cst, xst = login()
if not cst or not xst:
    exit()

min_size = get_min_deal_size(TEST_EPIC, cst, xst)
if min_size is None:
    exit()

if SIZE < min_size:
    print(f"⚠️ 倉位小於最小下單要求（{min_size}），請調整")
else:
    place_order(TEST_EPIC, DIRECTION, SIZE, STOP_DISTANCE, LIMIT_DISTANCE, cst, xst)
