import requests
import json

# 用戶的 IG API 設定
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"  # 填寫您的 API Key
USERNAME = "LUCIFINIL"  # 填寫您的 IG 用戶名
PASSWORD = "S22334455s"  # 填寫您的 IG 密碼
ACCOUNT_ID = "QL5HA"  # 填寫您的 IG 帳戶 ID
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"  # 產品標的，如黃金，您可以根據需要修改

# 登錄 IG
def login_ig(api_key, username, password):
    url = "https://api.ig.com/gateway/deal/session"
    headers = {
        "X-IG-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "identifier": username,
        "password": password
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        cst = response.headers.get("CST")
        x_token = response.headers.get("X-SECURITY-TOKEN")
        print("✅ 登錄成功")
        return cst, x_token
    else:
        print("❌ 登錄失敗:", response.status_code, response.text)
        return None, None

# 設置掛單函數
def place_order(api_key, cst, x_security_token, product_epic, account_id="QL5HA"):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = {
        "X-IG-API-KEY": api_key,
        "CST": cst,
        "X-SECURITY-TOKEN": x_security_token,
        "Content-Type": "application/json",
        "Version": "2"
    }
    
    payload = {
        "epic": product_epic,
        "expiry": "-",  # CFD 需要設置 expiry 為 "-"
        "direction": "BUY",  # 設置市價單的方向，這裡是BUY
        "size": 0.2,  # 設置倉位大小（您可以調整）
        "orderType": "MARKET",  # 設置為市價單
        "guaranteedStop": False,
        "forceOpen": True,
        "currencyCode": "USD",
        "accountId": account_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        deal_ref = data.get("dealReference", "")
        print("✅ 正式倉下單成功！訂單參考代碼:", deal_ref)
        return deal_ref
    else:
        print("❌ 正式倉下單失敗，狀態碼:", response.status_code)
        print("錯誤內容:", response.text)
        return None

# 查詢訂單狀態
def check_order_status(api_key, cst, x_security_token, deal_reference):
    url = f"https://api.ig.com/gateway/deal/confirm/{deal_reference}"
    headers = {
        "X-IG-API-KEY": api_key,
        "CST": cst,
        "X-SECURITY-TOKEN": x_security_token,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ 訂單狀態:", response.json())
    else:
        print("❌ 查詢訂單狀態失敗，HTTP 狀態碼:", response.status_code)
        print("錯誤內容:", response.text)

# 主執行程式
if __name__ == "__main__":
    cst, x_token = login_ig(API_KEY, USERNAME, PASSWORD)  # 登錄 IG
    if cst and x_token:
        place_order(API_KEY, cst, x_token, PRODUCT_EPIC)  # 根據需求自動下單
        check_order_status(API_KEY, cst, x_token, "您的訂單參考代碼")  # 查詢訂單狀態
