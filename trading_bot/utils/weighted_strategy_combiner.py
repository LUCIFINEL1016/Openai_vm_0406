# ✅ weighted_strategy_combiner.py – 策略信心加權模組（含 logging）
import logging

def combine_strategy_weights(results: dict) -> str:
    """
    統整所有策略結果，根據信心值加總 BUY / SELL，決定最終方向

    :param results: dict，格式如下：
        {
            "strategy_1": {"direction": "BUY", "confidence": 0.8},
            "strategy_2": {"direction": "SELL", "confidence": 0.6},
            ...
        }
    :return: str – "BUY" / "SELL" / "HOLD"
    """
    try:
        buy_score = 0.0
        sell_score = 0.0

        for name, result in results.items():
            direction = result.get("direction")
            confidence = result.get("confidence", 0)
            if direction == "BUY":
                buy_score += confidence
            elif direction == "SELL":
                sell_score += confidence

            logging.debug(f"🔍 {name} | {direction} ({confidence})")

        logging.info(f"📊 總分：BUY={buy_score:.2f} | SELL={sell_score:.2f}")
        if buy_score > sell_score:
            return "BUY"
        elif sell_score > buy_score:
            return "SELL"
        else:
            return "HOLD"

    except Exception as e:
        logging.error(f"❌ 策略加權錯誤：{e}")
        return "HOLD"
