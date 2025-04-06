
from Live_Trading_System.AutoOrder_Fallback_EURUSD0329 import fallback_eurusd_order

# 測試觸發自動掛 EUR/USD 倉
if __name__ == "__main__":
    current_price = 1.0750  # 模擬價格
    fallback_eurusd_order(current_price, quantity=1.0)
