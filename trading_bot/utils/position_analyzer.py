# ✅ position_analyzer.py – 持倉分析模組（風險比 / 建議分析 / logging）
import logging

def analyze_position_risk(position: dict, threshold_ratio=2.0):
    """
    分析單一持倉風險與浮盈是否達標。

    :param position: dict，應包含 "market.epic", "position.profitLoss", "position.stopLevel"
    :param threshold_ratio: 建議出場的浮盈倍數門檻（預設為 2 倍止損）
    :return: dict 分析結果，如建議是否出場、風險比率等
    """
    try:
        epic = position.get("market", {}).get("epic", "UNKNOWN")
        pnl = position.get("position", {}).get("profitLoss", 0.0)
        stop = abs(position.get("position", {}).get("stopLevel", 1.0))

        if stop == 0:
            logging.warning(f"⚠️ {epic} 無效止損距離，無法評估風險")
            return {"epic": epic, "suggest_exit": False, "note": "Stop=0"}

        ratio = pnl / stop
        suggest = ratio >= threshold_ratio

        logging.info(f"📊 {epic} | 浮盈：{pnl:.2f} | 止損：{stop:.2f} | 比率：{ratio:.2f} | 建議出場：{suggest}")
        return {
            "epic": epic,
            "pnl": pnl,
            "stop": stop,
            "ratio": round(ratio, 2),
            "suggest_exit": suggest
        }

    except Exception as e:
        logging.error(f"❌ 風險分析錯誤：{e}")
        return {"epic": "UNKNOWN", "suggest_exit": False, "note": str(e)}
