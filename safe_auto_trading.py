
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

# 檢查產品是否可交易與最小倉位
def is_product_tradeable(epic, cst, xst):
    url = f"https://api.ig.com/gateway/deal/markets/{epic}"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False, "查詢失敗"
    data = res.json()
    min_size = float(data["dealingRules"]["minDealSize"]["value"])
    market_status = data["snapshot"]["marketStatus"]
    stream_available = data["snapshot"]["streamingPricesAvailable"]
    if market_status != "TRADEABLE" or not stream_available:
        return False, "不可交易或無報價"
    return True, min_size

# 查詢帳戶資金
def get_account_cash(cst, xst):
    url = "https://api.ig.com/gateway/deal/accounts"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        accounts = res.json()["accounts"]
        for acc in accounts:
            if acc["accountId"] == ACCOUNT_ID:
                return float(acc["available"])
    return 0.0

# 下市價單函數（包含止盈止損與風控）
def place_order(epic, direction, cst, xst):
    ok, min_size = is_product_tradeable(epic, cst, xst)
    if not ok:
        print(f"🚫 無法交易 {epic}，原因：{min_size}")
        return

    cash = get_account_cash(cst, xst)
    risk_per_trade = 50  # 每筆最多風險承受 USD 50
    price_per_unit = 10  # 假設每 0.1 手約需 10 USD 保證金（需根據產品動態獲得）
    size = min_size
    while size * price_per_unit < risk_per_trade and size < 5:
        size += min_size

    if size * price_per_unit > cash:
        print(f"🚫 資金不足，無法開倉 {epic}，可用資金：{cash}")
        return

    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = HEADERS.copy()
    headers["CST"] = cst
    headers["X-SECURITY-TOKEN"] = xst

    payload = {
        "epic": epic,
        "expiry": "-",
        "direction": direction,
        "size": round(size, 2),
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
        deal_ref = res.json().get("dealReference", "")
        print(f"✅ {epic} 建倉成功 | 方向: {direction} | 倉位: {size} | 代碼: {deal_ref}")
        return deal_ref
    else:
        print(f"❌ 下單失敗（{epic}）: {res.status_code} - {res.text}")
        return None

# 查驗持倉風控完整性
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
                print(f"⚠️ 倉位缺風控：{epic}，建議立即補上止盈止損！")
    else:
        print(f"❌ 查詢倉位失敗：{res.status_code}")

# 主程序
def run():
    print("📌 自動交易啟動中 ...", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cst, xst = login()
    if not cst or not xst:
        return
    for p in PRODUCTS:
        place_order(p["epic"], p["direction"], cst, xst)
    audit_open_positions(cst, xst)

if __name__ == "__main__":
    run()
