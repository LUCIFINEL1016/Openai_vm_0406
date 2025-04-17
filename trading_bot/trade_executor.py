# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
# ✅ trade_executor.py — 下單執行模組（Confirm + tick fallback）

import uuid, logging
import numpy as np
import time

def execute_trade(ig_client, asset_code, direction):
    try:
        epic = ig_client.get_epic(asset_code)
        if not epic:
            logging.warning(f"❌ 無效資產代碼：{asset_code}")
            return

        size = 1.0
        currency = "USD"
        expiry = "-"
        # ✅ 檢查 expiry 參數是否正確
        if expiry != "-":
            logging.error(f"❌ 異常 expiry 參數：{expiry}，應為 '-'（CFD 帳戶）")
            return

        force_open = True
        guaranteed_stop = False
        order_type = "MARKET"
        level = None
        limit_distance = None

        fallback_ticks = [50, 60, 70, 80, 100, 120]
        tick_size = ig_client.get_tick_size(asset_code)

        for ticks in fallback_ticks:
            stop_distance = tick_size * ticks
            deal_ref = uuid.uuid4().hex[:20]

            payload = {
                "epic": epic,
                "direction": direction,
                "size": size,
                "orderType": order_type,
                "currencyCode": currency,
                "expiry": expiry,
                "forceOpen": force_open,
                "guaranteedStop": guaranteed_stop,
                "level": level,
                "limitDistance": limit_distance,
                "stopDistance": stop_distance,
                "dealReference": deal_ref
            }

            logging.info(f"📤 下單嘗試（{ticks} ticks）：{payload}")

            resp = ig_client.place_order(payload)
            if resp and resp.get("dealReference"):
                confirm = ig_client.check_deal_confirmation(resp["dealReference"])
                if confirm.get("status") == "ACCEPTED":
                    logging.info(f"✅ 成功下單：{asset_code} ({direction}) @ tick {ticks}")
                    return True
                else:
                    logging.warning(f"⏸ Confirm 拒絕：{confirm}")
            else:
                logging.warning(f"⛔ 下單失敗，嘗試 fallback 下個 tick 距離")

            time.sleep(1)

        logging.error(f"❌ 全部 fallback 嘗試失敗，跳過此單：{asset_code}")
        return False

    except Exception as e:
        logging.error(f"❌ 下單模組錯誤（{asset_code}）：{e}")
        return False

def safe_execute_trade(ig, asset, direction, max_retries=3, retry_delay=5):
    for attempt in range(1, max_retries + 1):
        try:
            success = execute_trade(ig, asset, direction)
            if success:
                logging.info(f"✅ 下單成功（第 {attempt} 次）")
                return True
        except Exception as e:
            logging.warning(f"⚠️ 第 {attempt} 次下單錯誤：{e}")
        time.sleep(retry_delay)
    logging.error(f"❌ 補單失敗：已達重試上限 {max_retries} 次")
    return False
