from dotenv import load_dotenv 
import os
import requests
import logging
import random
from datetime import datetime

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取配置
API_KEY = os.getenv('LIVE_IG_API_KEY')  # 从 .env 文件读取 API_KEY
USERNAME = os.getenv('LIVE_IG_USERNAME')  # 从 .env 文件读取 USERNAME
PASSWORD = os.getenv('LIVE_IG_PASSWORD')  # 从 .env 文件读取 PASSWORD
ACCOUNT_ID = os.getenv('LIVE_IG_ACC_ID')  # 从 .env 文件读取 ACCOUNT_ID
MIN_DAILY_PROFIT = 1000  # 最小每日目标利润 (HKD)

HEADERS = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 定义要交易的产品列表
PRODUCTS = [
    {"epic": "CS.D.CFDGOLD.CFDGC.IP", "name": "GOLD", "direction": "BUY"},
    {"epic": "CS.D.NATGAS.CFD.IP", "name": "NATGAS", "direction": "SELL"},
    {"epic": "IX.D.NASDAQ.IFD.IP", "name": "NASDAQ", "direction": "BUY"},
    {"epic": "CS.D.AAPL.CFD.IP", "name": "APPLE", "direction": "BUY"},
    {"epic": "CS.D.EURUSD.CFD.IP", "name": "EUR/USD", "direction": "SELL"}
]

# 设置日志记录
logging.basicConfig(filename='trading_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# 登录到 IG API 获取 CST 和 X-Security-Token
def login_ig():
    url = "https://api.ig.com/gateway/deal/session"
    payload = {"identifier": USERNAME, "password": PASSWORD}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        cst = response.headers.get("CST")
        x_token = response.headers.get("X-SECURITY-TOKEN")
        logging.info("Login successful")
        return cst, x_token
    else:
        logging.error(f"Login failed: {response.status_code}")
        return None, None

# 动态获取交易产品的 EPIC
def fetch_product_epic():
    return random.choice([p["epic"] for p in PRODUCTS])

# 下单操作，选择交易产品和方向
def place_order(cst, x_token, epic, direction, size=0.2):
    url = "https://api.ig.com/gateway/deal/positions/otc"
    payload = {
        "epic": epic,
        "direction": direction,
        "size": size,
        "orderType": "MARKET",
        "currencyCode": "USD",
        "accountId": ACCOUNT_ID,
        "guaranteedStop": False,  # 禁用保证止损
        # 可选：可以在需要时设置到期时间等其他参数
        # "expiry": "2025-04-07T00:00:00Z"  # 示例设置到期时间
    }

    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": x_token,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        logging.info(f"Order placed successfully: {epic} - {direction} - Size: {size}")
        return response.json().get("dealReference", "")
    else:
        logging.error(f"Order failed for {epic}: {response.text}")
        return None

# 跟踪每日利润，并决定是否继续交易
def track_profit_and_continue(current_profit, target_profit, market_conditions, position_status):
    """
    此函数跟踪利润并检查目标利润是否已达到。
    如果目标已达到，则根据市场条件和头寸管理继续下单。
    
    :param current_profit: 当前累计的利润
    :param target_profit: 用户设置的目标利润
    :param market_conditions: 当前的市场条件，用于判断是否下单
    :param position_status: 当前头寸状态（开盘/平仓）
    """
    # 检查当前利润是否已达到或超过目标利润
    if current_profit >= target_profit:
        logging.info(f"Target profit reached: {current_profit} HKD")

        # 根据市场条件和头寸状态继续下单
        if market_conditions == "bullish" and position_status == "open":
            logging.info("Market is bullish. Consider adding to the position.")
            # 根据策略在市场看涨时增加仓位

        elif market_conditions == "bearish" and position_status == "open":
            logging.info("Market is bearish. Consider reducing the position or placing stop orders.")
            # 根据策略在市场看跌时减少仓位或设置止损

        else:
            logging.info("Market conditions are neutral. Maintain current position.")
            # 根据其他因素保持当前头寸

    else:
        logging.info("Target profit not yet reached. Continue with the current trading strategy.")
        # 继续按照当前交易策略执行

# 动态调整仓位大小（风险管理）
def calculate_trade_size():
    return 0.2  # 示例：小仓位的风险管理

# 主函数：管理每日交易
def manage_daily_trading():
    cst, x_token = login_ig()
    if not cst or not x_token:
        return

    current_profit = 1200  # 模拟当前利润 (HKD)
    market_conditions = "bullish"  # 示例市场条件
    position_status = "open"  # 当前头寸状态

    # 跟踪利润并决定是否继续交易
    track_profit_and_continue(current_profit, MIN_DAILY_PROFIT, market_conditions, position_status)

    for product in PRODUCTS:
        epic = product["epic"]
        direction = product["direction"]
        size = calculate_trade_size()

        place_order(cst, x_token, epic, direction, size)

# 运行系统（调度每日交易）
if __name__ == "__main__":
    manage_daily_trading()
