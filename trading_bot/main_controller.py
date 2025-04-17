# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import os
import time
import zipfile
import logging
import importlib
import pandas as pd
from ig_api_client import IGClient
import strategy_bundle  # 策略池模組

# ✅ Logger 設定
logging.basicConfig(
    filename='/home/hmtf000001/auto_trading_team/logs/main_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def auto_backup():
    try:
        timestamp = time.strftime('%Y%m%d_%H%M')
        backup_name = f"/home/hmtf000001/backup_zips_generated/UnifiedTeam_Backup_{timestamp}.zip"
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("/home/hmtf000001/auto_trading_team"):
                for file in files:
                    if file.endswith((".py", ".json", ".txt")):
                        full_path = os.path.join(root, file)
                        zipf.write(full_path, arcname=os.path.relpath(full_path, "/home/hmtf000001/auto_trading_team"))
        logging.info(f"📦 已備份至：{backup_name}")
        logging.info("📦 自動備份完成")
    except Exception as e:
        logging.error(f"❌ 備份錯誤：{e}")
        logging.debug(f"Traceback: {e}")

def main():
    logger = logging.getLogger(__name__)
    logger.info("🔁 啟動 Unified-Team-v2.4.6-AutoOrderEnabled")

    # ✅ 初始化 IG API
    ig = IGClient()
    if not ig.login():
        logger.error("❌ IG 登入失敗，系統結束")
        return
    logger.info("✅ IG 登入成功")

    try:
        importlib.reload(strategy_bundle)
        StrategyPool = strategy_bundle.StrategyPool
    except Exception as e:
        logger.error(f"❌ 策略池載入失敗 | {e}")
        return

    epic = "CS.D.GBPUSD.MINI.IP"

    try:
        logger.info("📦 StrategyPool evaluate_all 來源：strategy_bundle")
        prices = ig.get_price_history(epic)

        if prices is None or (isinstance(prices, pd.Series) and prices.empty):
            logger.warning(f"⚠️ {epic} 沒有有效價格資料，跳過策略池執行")
            return

        result = StrategyPool.evaluate_all(epic, ig, logger=logger)
        logger.info(f"📊 策略回傳結果：{result}")

        # ✅ 決策與自動下單流程
        try:
            directions = [v["direction"] for v in result.values() if v["confidence"] >= 0.7]
            decision = max(set(directions), key=directions.count) if directions else "HOLD"

            if decision in ["BUY", "SELL"]:
                logger.info(f"🚀 綜合決策：{decision}，準備送出下單請求")

                deal_ref = ig.place_order(
                    epic=epic,
                    direction=decision,
                    size=0.1,
                    stop_distance=20,
                    limit_distance=30
                )

                if deal_ref:
                    logger.info(f"✅ 下單成功，單號：{deal_ref}")
                else:
                    logger.warning("⚠️ 下單未成功，請檢查錯誤記錄")
            else:
                logger.info("⛔ 綜合決策為 HOLD，不進行交易")

        except Exception as e:
            logger.error(f"❗下單流程錯誤 | {e}")

    except Exception as e:
        logger.error(f"❗策略池執行失敗 | {e}")

    auto_backup()

if __name__ == "__main__":
    main()
