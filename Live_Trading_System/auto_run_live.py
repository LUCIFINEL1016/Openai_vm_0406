
from Live_Trading_System.AutoTrigger_ByPrice import run_price_trigger_loop

# 啟動自動價格觸發流程（每 15 秒檢查一次，連續 5 回合）
if __name__ == "__main__":
    run_price_trigger_loop(interval_sec=15, rounds=5)
