
import time
from Live_Trading_System.UnifiedOrderTrigger import trigger_order

# 模擬即時價格資料來源（真實情況應從 API 獲取）
def get_mock_price(symbol):
    mock_prices = {
        "GOLD": 3037.0,
        "USOIL": 6962.5,
        "EURUSD": 1.0810
    }
    return mock_prices.get(symbol.upper(), None)

# 設定觸發門檻
price_thresholds = {
    "GOLD": 3036.0,
    "USOIL": 6960.0,
    "EURUSD": 1.0800
}

# 倉位設定
default_quantity = {
    "GOLD": 0.5,
    "USOIL": 0.5,
    "EURUSD": 1.0
}

def run_price_trigger_loop(interval_sec=10, rounds=3):
    for _ in range(rounds):
        print("🔍 檢查價格中...")
        for symbol in price_thresholds:
            current_price = get_mock_price(symbol)
            if current_price and current_price > price_thresholds[symbol]:
                print(f"🚀 價格突破！{symbol} = {current_price} > {price_thresholds[symbol]}")
                trigger_order(symbol, price=current_price, quantity=default_quantity[symbol])
            else:
                print(f"{symbol} 尚未突破 ({current_price} ≤ {price_thresholds[symbol]})")
        time.sleep(interval_sec)

# 若需獨立執行此模組，請取消下列註解
# if __name__ == "__main__":
#     run_price_trigger_loop()
