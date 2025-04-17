# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled (經 AI 修改 V1)
import os
import time
import zipfile
import logging
import importlib
import pandas as pd # 雖然可能唔再直接用，但保留 import 以防策略池需要
from ig_api_client import IGClient
import strategy_bundle  # 策略池模組

# --- DEBUG ---
print("DEBUG: Script start")

# ✅ Logger 設定 (修正路徑為相對路徑)
log_dir = 'logs'
log_file = os.path.join(log_dir, 'main_log.txt')
try:
    os.makedirs(log_dir, exist_ok=True) # 確保 logs 文件夾存在
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    print(f"DEBUG: Logging configured to: {log_file}")
except Exception as e:
    print(f"FATAL: Failed to configure logging to {log_file}. Error: {e}")
    # 如果連日誌都設定唔到，可能需要停止程式
    exit(1) # 或者用其他方式處理

# --- DEBUG ---
print("DEBUG: Logging setup complete")


def auto_backup():
    # --- DEBUG ---
    print("DEBUG: auto_backup() function started")
    try:
        timestamp = time.strftime('%Y%m%d_%H%M')
        # 修正備份文件夾路徑，確保存在
        backup_dir = "/home/hmtf000001/backup_zips_generated"
        os.makedirs(backup_dir, exist_ok=True)
        backup_name = os.path.join(backup_dir, f"UnifiedTeam_Backup_{timestamp}.zip") # 修正變數結尾

        # --- DEBUG ---
        print(f"DEBUG: Backup target filename: {backup_name}")
        # 修正備份源路徑，改為當前目錄 "."
        source_dir = "."
        print(f"DEBUG: Backup source directory: {source_dir}")

        added_files_count = 0
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                # 避免遍歷 venv 和其他唔需要嘅目錄 (可以按需增加)
                dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'backup_zips_generated', 'logs']]

                for file in files:
                    # 只備份特定類型文件，避免壓縮過大文件或敏感文件
                    if file.endswith((".py", ".json", ".txt", ".sh", ".env")):
                        full_path = os.path.join(root, file)
                        # 使用相對於 source_dir 的路徑存入 zip
                        arcname = os.path.relpath(full_path, source_dir)
                        print(f"  DEBUG: adding: {arcname}") # 模仿 zip 輸出
                        zipf.write(full_path, arcname=arcname)
                        added_files_count += 1

        if added_files_count > 0:
            logging.info(f"📦 已備份 {added_files_count} 個文件至：{backup_name}")
            logging.info("📦 自動備份完成")
            print(f"DEBUG: Backup successful: {backup_name}")
        else:
            logging.warning("⚠️ 未找到符合條件的文件進行備份。")
            print("DEBUG: No files found to backup.")

    except Exception as e:
        logging.error(f"❌ 備份錯誤：{e}")
        # logging.debug(f"Traceback: {e}") # Debug 級別可能需要調整 logger level
        print(f"DEBUG: Exception during backup: {e}") # 直接打印異常
    # --- DEBUG ---
    print("DEBUG: auto_backup() function finished")


def main():
    # --- DEBUG ---
    print("DEBUG: main() function started")
    logger = logging.getLogger(__name__) # 獲取配置好嘅 logger
    logger.info("🔁 啟動 Unified-Team-v2.4.6-AutoOrderEnabled (經 AI 修改 V1)")

    # ✅ 初始化 IG API
    # --- DEBUG ---
    print("DEBUG: Preparing to create IGClient instance")
    try:
        ig = IGClient()
        print("DEBUG: IGClient instance created (login attempted in init)")
    except Exception as e:
        print(f"FATAL: Failed to create IGClient instance. Error: {e}")
        logger.error(f"❌ 無法初始化 IGClient: {e}")
        return # 無法繼續

    # 檢查登錄狀態 (使用 authenticated 屬性)
    # --- DEBUG ---
    print(f"DEBUG: Checking ig.authenticated status: {ig.authenticated}")
    if not ig.authenticated:
        logger.error("❌ IG 登入失敗 (authenticated is False)，系統結束")
        print("DEBUG: IG Login failed (authenticated is False), exiting.")
        return
    logger.info("✅ IG 登入成功")
    print("DEBUG: IG Login successful (authenticated is True)")

    # 載入策略池 (保持原有邏輯，但修正潛在 typo)
    try:
        # --- DEBUG ---
        print("DEBUG: Reloading strategy_bundle")
        importlib.reload(strategy_bundle)
        StrategyPool = strategy_bundle.StrategyPool # 確保喺同一行或者分開
        print("DEBUG: StrategyPool loaded from strategy_bundle")
    except AttributeError:
         logger.error("❌ 策略池載入失敗: strategy_bundle 模組缺少 StrategyPool 屬性")
         print("DEBUG: Failed to load StrategyPool: AttributeError")
         return
    except Exception as e:
        logger.error(f"❌ 策略池載入失敗 | {e}")
        print(f"DEBUG: Failed to load StrategyPool: {e}")
        return

    # --- 暫時只處理單一商品 ---
    epic = "CS.D.GBPUSD.MINI.IP"
    print(f"DEBUG: Processing hardcoded epic: {epic}")

    # --- 獲取價格、執行策略、決策、落單 (暫時跳過，因 IGClient 缺少方法) ---
    # --- DEBUG ---
    print("DEBUG: Skipping price history, strategy evaluation and order placement due to missing IGClient methods (get_price_history, place_order)")
    logger.info("ℹ️ [暫時跳過] 價格獲取、策略評估、下單流程 (需實現對應 IGClient 方法)")

    # 模擬一個結果，以便流程繼續 (如果需要測試後續部分)
    # decision = "HOLD" # 或者 "BUY" / "SELL" 用於測試

    """
    # === 原有價格獲取與策略執行邏輯 (暫時註釋) ===
    try:
        logger.info("📦 StrategyPool evaluate_all 來源：strategy_bundle")
        print("DEBUG: Attempting to call ig.get_price_history (METHOD DOES NOT EXIST)") # DEBUG
        prices = ig.get_price_history(epic) # <--- 這會報錯，除非 IGClient 有此方法

        if prices is None or (isinstance(prices, pd.Series) and prices.empty):
            logger.warning(f"⚠️ {epic} 沒有有效價格資料，跳過策略池執行")
            print(f"DEBUG: No valid price data for {epic}, skipping evaluation.")
            # return # 如果冇價格就唔備份？可以考慮係咪 return

        else: # 只有獲取到價格先執行策略
             print(f"DEBUG: Calling StrategyPool.evaluate_all for {epic}")
             result = StrategyPool.evaluate_all(epic, ig, logger=logger)
             logger.info(f"📊 策略回傳結果：{result}")
             print(f"DEBUG: StrategyPool.evaluate_all returned: {result}")

             # ✅ 決策與自動下單流程
             try:
                 print("DEBUG: Evaluating decision based on strategy results")
                 # 原有決策邏輯 (假設 result 格式正確)
                 directions = [v["direction"] for v in result.values() if v.get("confidence", 0) >= 80] # 使用 .get 更安全
                 decision = max(set(directions), key=directions.count) if directions else "HOLD"
                 print(f"DEBUG: Calculated decision: {decision}")

                 if decision in ["BUY", "SELL"]:
                     logger.info(f"🚀 綜合決策：{decision}，準備送出下單請求")
                     print(f"DEBUG: Preparing to place order: {decision}")

                     print("DEBUG: Attempting to call ig.place_order (METHOD DOES NOT EXIST - use create_position)") # DEBUG
                     deal_ref = ig.place_order( # <--- 這會報錯，應改為 create_position
                         epic=epic,
                         direction=decision,
                         size=0.1, # 硬編碼
                         stop_distance=20, # 硬編碼
                         limit_distance=30 # 硬編碼 (create_position 冇呢個參數)
                     )

                     # === 使用 create_position 的正確示例 (需要取消註釋並替換上面) ===
                     # print("DEBUG: Calling ig.create_position")
                     # order_result = ig.create_position(
                     #     epic=epic,
                     #     direction=decision,
                     #     size=0.1, # 硬編碼
                     #     stop_distance=20 # 硬編碼
                     # )
                     # deal_ref = order_result.get("deal_reference") if order_result.get("success") else None
                     # print(f"DEBUG: ig.create_position returned: {order_result}")
                     # === /示例 ===


                     if deal_ref: # 或者 if order_result.get("success"):
                         logger.info(f"✅ 下單成功，單號：{deal_ref}")
                         print(f"DEBUG: Order placed successfully, Ref: {deal_ref}")
                     else:
                         logger.warning("⚠️ 下單未成功，請檢查錯誤記錄")
                         print("DEBUG: Order placement failed")
                 else:
                     logger.info("⛔ 綜合決策為 HOLD，不進行交易")
                     print("DEBUG: Decision is HOLD, no trade.")

             except Exception as e:
                 logger.error(f"❗下單流程錯誤 | {e}")
                 print(f"DEBUG: Exception during decision/order process: {e}")

    except AttributeError as e:
         logger.error(f"❗屬性錯誤，可能係 IGClient 缺少方法: {e}")
         print(f"DEBUG: AttributeError during strategy execution (likely missing IGClient method): {e}")
    except Exception as e:
        logger.error(f"❗策略池執行失敗 | {e}")
        print(f"DEBUG: Exception during strategy execution: {e}")
    # === /原有邏輯註釋結束 ===
    """

    # --- 執行自動備份 (移到 main 函數結尾，確保總會執行) ---
    print("DEBUG: Preparing to call auto_backup")
    auto_backup()
    print("DEBUG: auto_backup call finished")

    # --- main 函數結束 ---
    print("DEBUG: main() function finished")
    logger.info("✅ [Main] 交易流程結束 (經 AI 修改 V1)")


if __name__ == "__main__":
    # --- DEBUG ---
    print("DEBUG: Script entry point (__name__ == '__main__')")
    main()
