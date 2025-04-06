
import sys
import os

# 強制添加 Trading_System 到 sys.path，確保可以導入 api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.clients import IG_API_KEY, IG_CST, IG_SECURITY_TOKEN

def fetch_market_data(symbol):
    """ 模擬獲取市場數據 """
    market_data = {
        "AAPL": {"price": 175.20, "volume": 10000},
        "TSLA": {"price": 695.50, "volume": 8000},
    }
    return market_data.get(symbol, None)
