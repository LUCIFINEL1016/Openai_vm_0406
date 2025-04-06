# 貼上代碼（右鍵貼上）
# 按 Ctrl+O 儲存，Enter
# 按 Ctrl+X 離開
import requests
import json
import time
from datetime import datetime

# IG API 認證資料
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 要交易的產品列表（可增刪）
PRODUCTS = [
    {"epic": "CS.D.CFDGOLD.CFDGC.IP", "name": "GOLD", "direction": "BUY"},
    {"epic": "CS.D.NATGAS.CFD.IP", "name": "NATGAS", "direction": "SELL"},
    {"epic": "IX.D.NASDAQ.IFD.IP", "name": "NASDAQ", "direction": "SELL"},
    {"epic": "CS.D.USDJPY.CFD.IP", "name": "USDJPY", "direction": "BUY"},
    {"epic": "CS.D.AAPL.CFD.IP", "name": "AAPL", "direction": "BUY"}
]

# 登入 IG API 並回傳 CST 與 X-SECURITY-TOKEN
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

# 下市價單函數（包含止盈止損）
def place_order(epic, direction, cst, xst):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst

    payload = {
        "epic": epic,
        "expiry": "-",  # CFD 帳戶
        "direction": direction,
        "size": 0.3,  # 小倉
        "orderType": "MARKET",
        "guaranteedStop": False,
        "forceOpen": True,
        "level": None,
        "limitDistance": 20,  # 止盈點
        "stopDistance": 10,   # 止損點
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        deal_ref = response.json().get("dealReference", "")
        print(f"✅ {epic} 建倉成功 | 方向: {direction} | 代碼: {deal_ref}")
        return deal_ref
    else:
        print(f"❌ 下單失敗（{epic}）: {response.status_code} - {response.text}")
        return None

# 稽核現有倉位：檢查是否設有止盈止損
def audit_open_positions(cst, xst):
    url = "https://api.ig.com/gateway/deal/positions"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        positions = res.json().get("positions", [])
        for p in positions:
            epic = p["market"]["epic"]
            limit = p["position"].get("limitLevel")
            stop = p["position"].get("stopLevel")
            if not limit or not stop:
                print(f"⚠️ 倉位缺風控：{epic}，建議立即修正止盈止損！")
    else:
        print(f"❌ 查詢倉位失敗：{res.status_code}")

# 主執行程式
def run():
    print("📌 自動交易啟動中 ...", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cst, xst = login()
    if not cst or not xst:
        return

    for p in PRODUCTS:
        place_order(p["epic"], p["direction"], cst, xst)

    audit_open_positions(cst, xst)

# 啟動
if __name__ == "__main__":
    run()
