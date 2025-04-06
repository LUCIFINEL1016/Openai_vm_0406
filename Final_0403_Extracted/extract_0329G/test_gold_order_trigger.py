
from Live_Trading_System.AutoOrder_Fallback_Gold0326D import fallback_gold_order

# 測試觸發自動掛單流程
if __name__ == "__main__":
    current_price = 3028  # 模擬當前價格
    fallback_gold_order(current_price, quantity=0.5)
