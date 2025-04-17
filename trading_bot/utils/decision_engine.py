# ✅ decision_engine.py – 策略綜合決策模組（支援 logging 與容錯）
import logging

def decide_final_action(strategy_results: dict) -> str:
    """
    根據策略池的回傳結果，依據加權平均信心選擇 BUY / SELL / HOLD

    :param strategy_results: {
        "GPT_SIGNAL": {"direction": "BUY", "confidence": 0.8},
        "RSI_MACD": {"direction": "SELL", "confidence": 0.7},
        ...
    }

    :return: 最終決策方向 "BUY" / "SELL" / "HOLD"
    """
    try:
        if not strategy_results:
            logging.warning("⚠️ 無策略結果輸入，預設 HOLD")
            return "HOLD"

        scores = {"BUY": 0.0, "SELL": 0.0}
        for name, result in strategy_results.items():
            direction = result.get("direction", "")
            confidence = result.get("confidence", 0)
            if direction in scores:
                scores[direction] += confidence
            logging.debug(f"🧮 加入策略：{name} | {direction} ({confidence})")

        logging.info(f"📊 綜合信心評估結果：{scores}")
        if scores["BUY"] > scores["SELL"]:
            return "BUY"
        elif scores["SELL"] > scores["BUY"]:
            return "SELL"
        else:
            return "HOLD"

    except Exception as e:
        logging.error(f"❌ 決策評估錯誤：{e}")
        return "HOLD"
