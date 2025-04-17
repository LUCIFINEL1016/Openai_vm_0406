# ✅ exit_signal_manager.py – 出場策略模組（含 logging 與多條件）
import logging
from datetime import datetime

def should_exit(position: dict, threshold=2.0, max_duration_minutes=480):
    """
    綜合出場條件：
    1. 浮盈 >= 止損 * 閾值（預設 2 倍）
    2. [可選] 持倉時間過久（預設 8 小時 / 480 分鐘）

    參數 position 格式：
    {
        "unrealized_profit": float,
        "stop_loss": float,
        "duration_minutes": int,        # optional
        "open_time": datetime object    # optional
    }
    """
    try:
        profit = position.get("unrealized_profit", 0)
        stop = abs(position.get("stop_loss", 1)) or 1

        if profit >= stop * threshold:
            logging.info(f"✅ 出場建議 | 浮盈達標：{profit:.2f} >= {threshold:.1f}x{stop:.2f}")
            return True

        # 判斷持倉時間（支援兩種來源）
        if "duration_minutes" in position:
            duration = position.get("duration_minutes", 0)
            if duration >= max_duration_minutes:
                logging.info(f"⏰ 出場建議 | 持倉超時：{duration} 分鐘")
                return True

        elif "open_time" in position:
            open_time = position.get("open_time")
            if isinstance(open_time, datetime):
                elapsed = (datetime.now() - open_time).total_seconds() / 60
                if elapsed >= max_duration_minutes:
                    logging.info(f"⏰ 出場建議 | 持倉已超過 {elapsed:.1f} 分鐘")
                    return True

        return False

    except Exception as e:
        logging.error(f"❌ 出場判斷錯誤：{e}")
        return False
