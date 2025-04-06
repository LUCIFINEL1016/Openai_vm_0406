import requests
import json
import time
from datetime import datetime

# 設定API參數
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"  # 請使用您的API Key
USERNAME = "LUCIFINIL"  # 請使用您的IG帳戶名
PASSWORD = "S22334455s"  # 請使用您的IG密碼
ACCOUNT_ID = "QL5HA"  # 請使用您的IG帳戶ID
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"  # 請根據需要修改為您要交易的產品（此處為黃金）

# 設定風險控制和止損止盈
STOP_LOSS = 10  # 設定止損點
TAKE_PROFIT = 20  # 設定止盈點

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
        print("登入成功!")
        return cst, x_token
    else:
        print("登入失敗:", response.status_code, response.text)
        return None, None

# 計算動態交易量（此示範以簡單的波動性為例）
def calculate_dynamic_position_size(account_balance=10000, volatility=0.02):
    position_size = account_balance * volatility  # 根據波動性計算倉位
    position_size = max(position_size, 0.1)  # 設定最低倉位為0.1手
    return position_size

# 設定止損和止盈
def set_stop_loss_and_take_profit(stop_loss=STOP_LOSS, take_profit=TAKE_PROFIT):
    print(f"止損設置為：{stop_loss}，止盈設置為：{take_profit}")

# 下單函數
def place_order(api_key, cst, x_token, product_epic, account_id):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    headers = {
        "X-IG-API-KEY": api_key,
        "CST": cst,
        "X-SECURITY-TOKEN": x_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    position_size = calculate_dynamic_position_size()  # 根據波動性動態設置交易量

    payload = {
        "epic": product_epic,
        "expiry": "-",
        "direction": "BUY",  # 設定為BUY，根據需要可以調整為SELL
        "size": position_size,  # 計算的交易量
        "orderType": "MARKET",
        "currencyCode": "USD",
        "accountId": account_id
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        deal_ref = data.get("dealReference", "")
        print(f"訂單下單成功! 訂單參考號碼：{deal_ref}")
        return deal_ref
    else:
        print(f"下單失敗, HTTP 狀態碼: {response.status_code}. 詳情: {response.text}")
        return None

# 檢查是否是周末或假期
def is_weekend_or_holiday():
    today = datetime.datetime.now()
    if today.weekday() >= 5:  # 0-4為週一至週五，5-6為週末
        print("今天是周末，跳過交易")
        return True
    # 可以額外擴充檢查假期（例如透過API檢查是否為假期）
    return False

# 設置定時自動下單
def schedule_daily_order():
    current_time = time.strftime("%H:%M:%S")
    target_time = "06:00:00"  # 設定每天6點前下單
    if current_time < target_time:
        print(f"系統將於 {target_time} 自動下單")
        return True
    else:
        print(f"今天已過了6點，請確認交易狀況")
        return False

# 綜合管理每日交易
def manage_daily_trading(api_key, cst, x_token):
    if not is_weekend_or_holiday():
        schedule_daily_order()
        place_order(api_key, cst, x_token, PRODUCT_EPIC, ACCOUNT_ID)
        set_stop_loss_and_take_profit(stop_loss=10, take_profit=20)  # 設置止損止盈

# 主執行程序
if __name__ == "__main__":
    cst, x_token = login_ig(API_KEY, USERNAME, PASSWORD)
    if cst and x_token:
        manage_daily_trading(API_KEY, cst, x_token)
