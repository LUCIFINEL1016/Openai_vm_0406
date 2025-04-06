
import requests
import json
from datetime import datetime, timezone, timedelta

# === IG 登入資訊 ===
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"

# === 產品配置 ===
PRODUCTS = [
    {"epic": "CS.D.CFDGOLD.CFDGC.IP", "name": "GOLD CFD", "direction": "BUY"},
    {"epic": "CS.D.GOLD.CFD.IP", "name": "GOLD", "direction": "BUY"},
    {"epic": "CS.D.USDJPY.CFD.IP", "name": "USDJPY", "direction": "SELL"},
    {"epic": "IX.D.NASDAQ.IFE.IP", "name": "US Tech 100", "direction": "BUY"},
    {"epic": "CS.D.EURUSD.MINI.IP", "name": "EURUSD Mini", "direction": "BUY"},
    {"epic": "CS.D.EURUSD.CFD.IP", "name": "EURUSD", "direction": "BUY"},
    {"epic": "CC.D.WTI.CFM.IP", "name": "US Crude Oil", "direction": "BUY"},
    {"epic": "IX.D.NASDAQ.WK1.IP", "name": "Weekend US Tech", "direction": "BUY"},
]

# === 登入函數 ===
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
        print("✅ 登入成功")
        return res.headers["CST"], res.headers["X-SECURITY-TOKEN"]
    else:
        print("❌ 登入失敗", res.status_code, res.text)
        return None, None

# === 下單函數 ===
def place_order(epic, direction, cst, xst):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = {
        "X-IG-API-KEY": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Version": "2"
    }
    payload = {
        "epic": epic,
        "expiry": "-",
        "direction": direction,
        "size": 0.2,
        "orderType": "MARKET",
        "guaranteedStop": False,
        "forceOpen": True,
        "currencyCode": "USD",
        "limitDistance": 20,
        "stopDistance": 10,
        "accountId": ACCOUNT_ID
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        deal_ref = res.json().get("dealReference", "")
        print("✅ 建倉成功 | EPIC:", epic, "| 方向:", direction, "| 代碼:", deal_ref)
    else:
        print("❌ 建倉失敗 | EPIC:", epic, "| 錯誤:", res.status_code, res.text)

# === 市場開放檢查 ===
def is_market_open():
    now = datetime.now().astimezone(timezone(timedelta(hours=8)))
    return now.weekday() < 5  # 週一至週五為交易日

# === 主流程 ===
def run():
    print("📌 自動交易任務啟動時間：", datetime.now())
    if not is_market_open():
        print("🚫 市場休市，今日不執行交易")
        return
    cst, xst = login()
    if not cst or not xst:
        return
    for p in PRODUCTS:
        place_order(p["epic"], p["direction"], cst, xst)

# === 主程式執行點 ===
if __name__ == "__main__":
    run()
