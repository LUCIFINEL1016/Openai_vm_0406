# 版本標籤：Unified-Team-v2.4.6 (經 AI 修改 V4 - APScheduler 多輪制)
import os
import time
import zipfile
import logging
import logging.handlers
import importlib
import pandas as pd
from ig_api_client import IGClient
import strategy_bundle  # 策略池模組
from product_filter import get_target_products
# from risk_tuner import get_risk_config # 需要時取消註釋
from apscheduler.schedulers.blocking import BlockingScheduler # 新增：導入 APScheduler
from apscheduler.triggers.interval import IntervalTrigger # 如果需要更精確控制
from datetime import datetime
import pytz # 處理時區
from risk_tuner import get_risk_config         # 用於獲取風險配置，例如止損距離
from strategy_success_tracker import log_strategy_result # 用於記錄每次嘗試嘅結果
from collections import Counter                 # 用於決策邏輯中計票
# import time # 如果你想喺循環中加 sleep

# --- DEBUG ---
print("DEBUG: Script start")

# ✅ Logger 設定 (使用相對路徑)
log_dir = 'logs'
log_file = os.path.join(log_dir, 'main_log.txt')
try:
    os.makedirs(log_dir, exist_ok=True)
    # 使用 RotatingFileHandler 避免日誌文件無限增大 (示例)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3) # 例如：最大 5MB，保留 3 個備份
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger() # 獲取 root logger
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    # 如果想同時喺 console 輸出，可以加 StreamHandler
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(log_formatter)
    # logger.addHandler(console_handler)

    print(f"DEBUG: Logging configured to: {log_file} with rotation")
except Exception as e:
    print(f"FATAL: Failed to configure logging to {log_file}. Error: {e}")
    exit(1)

# --- DEBUG ---
print("DEBUG: Logging setup complete")


def auto_backup():
    # (auto_backup 函數內容不變，但建議之後由 Cron 或獨立排程處理，暫時保留喺度但唔會喺交易循環調用)
    # --- DEBUG ---
    print("DEBUG: auto_backup() function started")
    try:
        timestamp = time.strftime('%Y%m%d_%H%M')
        backup_dir = "/home/hmtf000001/backup_zips_generated"
        os.makedirs(backup_dir, exist_ok=True)
        backup_name = os.path.join(backup_dir, f"UnifiedTeam_Backup_{timestamp}.zip")

        print(f"DEBUG: Backup target filename: {backup_name}")
        source_dir = "."
        print(f"DEBUG: Backup source directory: {source_dir}")

        added_files_count = 0
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', '.cache', '.config', '.local']]
                for file in files:
                    if file.endswith((".py", ".json", ".txt", ".sh")) or file == ".env" or file == "requirements.txt":
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, source_dir)
                        try:
                            zipf.write(full_path, arcname=arcname)
                            added_files_count += 1
                        except Exception as zip_e: # 更具體咁捕捉 zip 錯誤
                            logger.warning(f"⚠️ 備份跳過：{full_path} | 錯誤: {zip_e}")
                            print(f"DEBUG: Backup skipped: {full_path} | Error: {zip_e}")

        if added_files_count > 0:
            logger.info(f"📦 已備份 {added_files_count} 個文件至：{backup_name}")
            print(f"DEBUG: Backup successful: {backup_name}")
        else:
            logger.warning("⚠️ 未找到符合條件的文件進行備份。")
            print("DEBUG: No files found to backup.")

    except Exception as e:
        logger.error(f"❌ 備份函數錯誤：{e}")
        print(f"DEBUG: Exception during backup function: {e}")
    print("DEBUG: auto_backup() function finished")


# (文件頂部嘅 import 和 auto_backup 函數保持不變)

def run_trading_cycle(ig_client, strategy_pool, logger):
    """
    執 行 一 輪 交 易 邏 輯 的 核 心 函 數
    (被 APScheduler 定時調用)
    """
    # --- DEBUG ---

    # --- 新增：獲取當前 HKT 時間並檢查是否週末 ---
    hkt_timezone = pytz.timezone('Asia/Hong_Kong')
    now_hkt = datetime.now(hkt_timezone)
    print(f"\nDEBUG: ----- Checking Trading Cycle Start at {now_hkt.strftime('%Y-%m-%d %H:%M:%S %Z')} -----")

    # datetime.weekday() 返回星期一係 0，星期日係 6
    if now_hkt.weekday() >= 5: # 5 代表星期六, 6 代表星期日
         logger.info(f"😴 市場休市時間 ({now_hkt.strftime('%A')})，跳過本輪交易檢查。")
         print(f"DEBUG: Weekend ({now_hkt.strftime('%A')}), skipping trading cycle.")
         return # 直接退出本次函數調用，唔執行後面嘅邏輯
    # --- /新增檢查 ---

    # 如果唔係週末，先繼續執行原有邏輯
    logger.info("========== 執行新一輪交易檢查 ==========")

    # 檢查 IG 登錄狀態 (保留原有檢查)
    if not ig_client.authenticated:
         # ... (relogin attempt or return) ...
         return

    # 獲取目標產品列表
    # ... (函數後面嘅所有原有代碼保持不變) ...

    print(f"\nDEBUG: ----- Starting Trading Cycle at {datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime('%Y-%m-%d %H:%M:%S %Z')} -----")
    logger.info("========== 執行新一輪交易檢查 ==========")

    # 檢查 IG 登錄狀態
    if not ig_client.authenticated:
         logger.error("❌ IG 未登錄，跳過此輪交易檢查。嘗試重新登錄...")
         print("DEBUG: IG Client not authenticated, attempting relogin...")
         ig_client._login() # 嘗試重新登錄
         if not ig_client.authenticated:
             logger.error("❌ 重新登錄失敗，繼續跳過。")
             print("DEBUG: Relogin failed, skipping cycle.")
             return # 登錄失敗就退出本次循環

    # 獲取目標產品列表
    print("DEBUG: Calling get_target_products")
    try:
        products = get_target_products()
        print(f"DEBUG: Target products loaded: {products}")
    except Exception as e:
        logger.error(f"❌ 無法獲取產品列表: {e}", exc_info=True)
        print(f"DEBUG: Failed to get products in cycle: {e}")
        products = []

    if not products:
        logger.warning("⚠️ 未找到目標產品，跳過此輪交易檢查。")
        print("DEBUG: No products found, skipping cycle.")
        return

    # 遍歷產品列表
    print("DEBUG: Starting product loop for this cycle...")
    for epic in products:
        print(f"DEBUG: === Processing epic: {epic} ===")
        logger.info(f"  ➡️ 開始處理商品: {epic}")
        cycle_status = "UNKNOWN" # 用於記錄最終狀態

        try:
            # --- 步驟 1: 獲取價格歷史 ---
            logger.info(f"  📦 [{epic}] 獲取價格數據...")
            print(f"DEBUG: [{epic}] Attempting to call ig_client.get_price_history")
            # 調用我哋新加嘅方法 (注意：resolution 和 num_points 可能需要根據策略調整)
            prices = ig_client.get_price_history(epic, resolution='DAY', num_points=20)

            # 檢查價格數據是否有效
            if prices is None or not isinstance(prices, pd.Series) or prices.empty:
                logger.warning(f"  ⚠️ [{epic}] 沒有有效價格資料，跳過此商品。")
                print(f"DEBUG: [{epic}] No valid price data received, skipping epic.")
                cycle_status = "NO_DATA"
                log_strategy_result(epic, cycle_status) # 記錄跳過原因
                continue # 處理下一個 epic

            # --- 步驟 2: 執行策略評估 ---
            # 注意：策略目前仍然係返回隨機結果嘅 placeholder
            print(f"DEBUG: [{epic}] Calling StrategyPool.evaluate_all")
            # 假設 evaluate_all 返回 {'strategy_name': {'direction': 'BUY'/'SELL'/'HOLD', 'confidence': 85}, ...}
            result = strategy_pool.evaluate_all(epic, ig_client, logger=logger) # 可能需要傳入價格數據 prices
            logger.info(f"  📊 [{epic}] 策略回傳結果(模擬): {result}")
            print(f"DEBUG: [{epic}] StrategyPool.evaluate_all returned: {result}")

            # --- 步驟 3: 進行交易決策 ---
            try:
                print(f"DEBUG: [{epic}] Evaluating decision")
                # 過濾有效信號 (信心度 >= 80 且方向為 BUY/SELL)
                valid_signals = [v for v in result.values() if isinstance(v, dict) and v.get("confidence", 0) >= 80 and v.get("direction") in ["BUY", "SELL"]]
                directions = [v["direction"] for v in valid_signals]

                decision = "HOLD" # 預設為 HOLD
                if directions:
                    # 簡單多數票決策邏輯
                    direction_counts = Counter(directions)
                    max_count = 0
                    top_directions = []
                    for direction, count in direction_counts.items():
                        if count > max_count:
                            max_count = count
                            top_directions = [direction]
                        elif count == max_count:
                            top_directions.append(direction)
                    # 只有唯一嘅多數方向先採納
                    if len(top_directions) == 1:
                        decision = top_directions[0]

                print(f"DEBUG: [{epic}] Calculated decision: {decision}")

                # --- 步驟 4: 如果決策係 BUY/SELL，執行落單 ---
                if decision in ["BUY", "SELL"]:
                    logger.info(f"  🚀 [{epic}] 綜合決策：{decision}，準備送出下單請求")
                    print(f"DEBUG: [{epic}] Preparing to place order: {decision}")

                    # 獲取風險配置
                    print(f"DEBUG: [{epic}] Calling get_risk_config")
                    try:
                        risk = get_risk_config(epic)
                        stop_distance = risk.get("default_stop", 30) # 從配置獲取止損
                        # TODO: size 需要根據 risk.get("max_risk_per_trade") 和止損距離計算，暫時用 1
                        size = 1
                        print(f"DEBUG: [{epic}] Risk config loaded: stop_distance={stop_distance}, calculated_size={size} (hardcoded)")
                    except Exception as risk_e:
                         logger.error(f"❗[{epic}] 獲取風險配置失敗: {risk_e}", exc_info=True)
                         print(f"DEBUG: [{epic}] Failed to get risk config: {risk_e}")
                         cycle_status = "EXCEPTION_RISK"
                         log_strategy_result(epic, cycle_status)
                         continue # 無法獲取風險配置，跳過此產品

                    # 調用正確嘅 create_position 方法
                    print(f"DEBUG: [{epic}] Calling ig_client.create_position with size={size}, stop={stop_distance}")
                    order_result = ig_client.create_position(
                         epic=epic,
                         direction=decision,
                         size=size,
                         stop_distance=stop_distance
                     )
                    print(f"DEBUG: [{epic}] ig_client.create_position returned: {order_result}")

                    # 記錄落單結果
                    if order_result.get("success"):
                         deal_ref = order_result.get("deal_reference")
                         logger.info(f"  ✅ [{epic}] 下單成功，單號：{deal_ref}")
                         print(f"DEBUG: [{epic}] Order placed successfully, Ref: {deal_ref}")
                         cycle_status = "SUCCESS"
                    else:
                         logger.warning(f"  ⚠️ [{epic}] 下單未成功，錯誤: {order_result.get('error')}")
                         print(f"DEBUG: [{epic}] Order placement failed: {order_result.get('error')}")
                         cycle_status = "FAIL"
                else:
                     # 決策為 HOLD 或其他情況
                     logger.info(f"  ⛔ [{epic}] 綜合決策為 {decision}，不進行交易")
                     print(f"DEBUG: [{epic}] Decision is {decision}, no trade.")
                     cycle_status = "SKIP_" + decision # 例如 SKIP_HOLD

            except Exception as e:
                 logger.error(f"❗[{epic}] 決策或下單流程錯誤 | {e}", exc_info=True)
                 print(f"DEBUG: [{epic}] Exception during decision/order process: {e}")
                 cycle_status = "EXCEPTION_ORDER"

        except AttributeError as e:
             # 特別捕捉 IGClient 缺少方法嘅錯誤
             logger.error(f"❗[{epic}] 屬性錯誤 (可能 IGClient 缺少方法或 API 問題): {e}", exc_info=True)
             print(f"DEBUG: [{epic}] AttributeError (likely missing method or API issue): {e}")
             cycle_status = "EXCEPTION_ATTR"
        except Exception as e:
             # 捕捉處理單個 epic 時嘅其他未預期錯誤
             logger.error(f"❗處理商品 {epic} 時發生未預期錯誤 | {e}", exc_info=True)
             print(f"DEBUG: [{epic}] Unhandled exception during processing: {e}")
             cycle_status = "EXCEPTION_EPIC"

        # 記錄呢個 epic 最終嘅執行狀態
        log_strategy_result(epic, cycle_status)
        print(f"DEBUG: === Finished processing epic: {epic} with status: {cycle_status} ===")
        # 可以考慮喺處理完一個 epic 後稍微暫停一下，避免過於頻繁請求 API
        # print("DEBUG: Sleeping for 0.5 seconds...")
        # time.sleep(0.5)

    # --- 產品循環結束 ---
    print("DEBUG: Product loop finished for this cycle")
    logger.info("========== 本輪交易檢查結束 ==========")

# (main 函數同埋 if __name__ == "__main__": 部分保持不變)

def main():
    # --- DEBUG ---
    print("DEBUG: main() function started (APScheduler version)")
    logger = logging.getLogger() # 獲取 root logger
    logger.info("🚀 系統啟動 (APScheduler 多輪制)")

    # ✅ 初始化 IG API Client (只需要一次)
    print("DEBUG: Preparing to create SINGLE IGClient instance for scheduler")
    try:
        ig = IGClient() # 登錄喺 __init__ 嘗試
        print("DEBUG: IGClient instance created")
    except Exception as e:
        print(f"FATAL: Failed to create IGClient instance. Error: {e}")
        logger.critical(f"❌ 無法初始化 IGClient，系統無法啟動: {e}")
        return

    # 檢查首次登錄
    if not ig.authenticated:
        logger.critical("❌ IG 首次登錄失敗，系統無法啟動。請檢查憑證或網絡。")
        print("DEBUG: Initial IG Login failed, scheduler will not start.")
        return
    logger.info("✅ IG 首次登錄成功，準備啟動排程器。")
    print("DEBUG: Initial IG Login successful.")

    # ✅ 載入策略池 (只需要一次)
    try:
        print("DEBUG: Reloading strategy_bundle for initial load")
        importlib.reload(strategy_bundle)
        StrategyPool = strategy_bundle.StrategyPool
        print("DEBUG: StrategyPool loaded from strategy_bundle")
    except Exception as e:
        logger.critical(f"❌ 無法載入策略池，系統無法啟動: {e}")
        print(f"DEBUG: Failed to load StrategyPool, scheduler will not start: {e}")
        return

    # ✅ 配置並啟動 APScheduler
    try:
        scheduler = BlockingScheduler(timezone='Asia/Hong_Kong') # 設置時區為 HKT

        # 添加交易循環任務，例如每 10 分鐘執行一次
        run_interval_minutes = 10
        scheduler.add_job(run_trading_cycle,
                          trigger='interval',
                          minutes=run_interval_minutes,
                          args=[ig, StrategyPool, logger], # 將初始化好嘅對象傳入
                          id='trading_cycle_job',
                          name='Run Trading Logic Cycle',
                          next_run_time=datetime.now(pytz.timezone('Asia/Hong_Kong')) # 可以設置立即運行一次
                         )
        logger.info(f"🕒 排程器已設定，交易循環將每 {run_interval_minutes} 分鐘運行一次。")
        print(f"DEBUG: Scheduler configured to run run_trading_cycle every {run_interval_minutes} minutes.")

        # 喺呢度可以添加其他排程任務，例如每日定時備份
        # scheduler.add_job(auto_backup, trigger='cron', hour=23, minute=55, id='daily_backup_job', name='Daily Auto Backup')
        # logger.info("🕒 已添加每日自動備份任務 (23:55 HKT)")
        # print("DEBUG: Daily backup job added to scheduler.")

        print("DEBUG: Starting scheduler...")
        logger.info("▶️ 排程器啟動，系統進入持續運行模式...")
        scheduler.start() # 呢個會阻塞，直到排程器停止

    except KeyboardInterrupt:
        logger.info("⏹️ 收到停止信號 (KeyboardInterrupt)，關閉排程器...")
        print("\nDEBUG: KeyboardInterrupt received, shutting down scheduler.")
        if scheduler.running:
             scheduler.shutdown()
    except Exception as e:
        logger.critical(f"❌ 排程器運行出錯，系統停止: {e}", exc_info=True) # 記錄 traceback
        print(f"FATAL: Scheduler error: {e}")
        # 可能需要喺呢度添加通知機制


# 文件最底部的入口點
if __name__ == "__main__":
    # --- DEBUG ---
    print("DEBUG: Script entry point (__name__ == '__main__')")
    main()
