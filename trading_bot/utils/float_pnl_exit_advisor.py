# ✅ float_pnl_exit_advisor.py – 浮盈出場建議模組（含 logging）
import logging

def should_take_profit(pnl: float, stop_distance: float, multiplier: float = 2.0) -> bool:
    """
    根據浮盈是否超過止損距離 x 倍數決定是否建議平倉。

    :param pnl: 當前浮盈
    :param stop_distance: 止損距離（正值）
    :param multiplier: 建議出場所需倍數（預設 2 倍）

    :return: bool，是否應該建議平倉
    """
    try:
        stop_distance = abs(stop_distance)
        if stop_distance == 0:
            logging.warning("⚠️ Stop distance 為 0，無法進行出場建議")
            return False

        if pnl >= stop_distance * multiplier:
            logging.info(f"✅ 浮盈平倉建議 | 浮盈 {pnl:.2f} 超過 {multiplier} 倍止損 {stop_distance:.2f}")
            return True

        logging.info(f"📉 未達出場標準 | 浮盈 {pnl:.2f} / 門檻 {stop_distance * multiplier:.2f}")
        return False

    except Exception as e:
        logging.error(f"❌ 浮盈出場判斷錯誤：{e}")
        return False
