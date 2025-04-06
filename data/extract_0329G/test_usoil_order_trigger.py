
from Live_Trading_System.AutoOrder_Fallback_USOIL0329 import fallback_oil_order

# 測試觸發自動掛原油倉
if __name__ == "__main__":
    current_price = 6957.3  # 模擬當前價格
    fallback_oil_order(current_price, quantity=0.5)
