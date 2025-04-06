import requests
import json
import time
import datetime
from newsapi import NewsApiClient

# 設定API參數
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"
USERNAME = "LUCIFINIL"
PASSWORD = "S22334455s"
ACCOUNT_ID = "QL5HA"
PRODUCT_EPIC = "CS.D.CFDGOLD.CFDGC.IP"  # 設定你想交易的產品（例如黃金）

# IG API 登入
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
        print("Login successful!")
        return cst, x_token
    else:
        print("Login failed:", response.status_code, response.text)
        return None, None

# 檢查API金鑰有效性
def check_api_validity():
    # 嘗試登入以確保API金鑰有效
    cst, x_token = login_ig(API_KEY, USERNAME, PASSWORD)
    if cst and x_token:
        return True
    else:
        return False

# 獲取市場新聞
def get_market_news():
    newsapi = NewsApiClient(api_key='your_news_api_key')
    top_headlines = newsapi.get_top_headlines(language='en', category='business')
    headlines = []
    for article in top_headlines['articles']:
        headlines.append(article['title'])
    return headlines

# 計算動態交易量（此示範以簡單的波動性為例）
def calculate_dynamic_position_size():
    volatility = 0.02  # 假設市場的波動率為 2%
    account_balance = 10000  # 假設帳戶餘額為 10,000 USD
    position_size = account_balance * volatility
    return position_size

# 設定止損和止盈
def set_stop_loss_and_take_profit(stop_loss=10, take_profit=20):
    # 假設這裡設置了止損和止盈的條件
    print(f"Stop loss set to: {stop_loss}, Take profit set to: {take_profit}")

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
    
    payload = {
        "epic": product_epic,
        "expiry": "-",
        "direction": "BUY",  # 或 "SELL" 根據需求
        "size": calculate_dynamic_position_size(),  # 根據波動性動態設置交易量
        "orderType": "MARKET",
        "currencyCode": "USD",
        "accountId": account_id
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        deal_ref = data.get("dealReference", "")
        print(f"Order placed successfully! Order reference number: {deal_ref}")
        return deal_ref
    else:
        print(f"Order failed, HTTP Status Code: {response.status_code}. Details: {response.text}")
        return None

# 檢查是否是周末或假期
def is_weekend_or_holiday():
    today = datetime.datetime.now()
    if today.weekday() >= 5:  # 0-4為週一至週五，5-6為週末
        print("Today is the weekend, placing an order for later execution.")
        return False  # 允許掛單
    return True  # 工作日返回 True，繼續下單

# 設置定時自動下單
def schedule_daily_order():
    current_time = time.strftime("%H:%M:%S")
    target_time = "06:00:00"  # 設定每天6點前下單
    if current_time < target_time:
        print(f"System will place order before {target_time}")
        return True
    else:
        print(f"Today is past 6 AM, please check trading status")
        return False

# 綜合管理每日交易
def manage_daily_trading(api_key, cst, x_token):
    if not is_weekend_or_holiday():  # 周末掛單
        print("Placing order for future execution on Monday.")
        return

    if not is_weekend_or_holiday():
        schedule_daily_order()
        place_order(api_key, cst, x_token, PRODUCT_EPIC, ACCOUNT_ID)
        set_stop_loss_and_take_profit(stop_loss=10, take_profit=20)  # 設置止損止盈

# 主執行程序
if __name__ == "__main__":
    cst, x_token = login_ig(API_KEY, USERNAME, PASSWORD)
    if cst and x_token:
        manage_daily_trading(API_KEY, cst, x_token)
