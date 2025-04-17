# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
from collections import Counter

def weighted_decision(strategy_results, logger=None):
    """
    根據策略結果的方向與信心度，加權做出綜合決策。
    :param strategy_results: dict，包含多個策略回傳的 direction 與 confidence
    :param logger: 可選 logger 實例
    :return: 綜合決策 direction（BUY / SELL / HOLD）
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    score = {"BUY": 0.0, "SELL": 0.0, "HOLD": 0.0}

    for name, result in strategy_results.items():
        direction = result.get("direction", "HOLD").upper()
        confidence = result.get("confidence", 0.0)

        logger.info(f"📊 策略 [{name}] → 決策：{direction}（信心度：{confidence}）")

        if direction in score:
            score[direction] += confidence
        else:
            score["HOLD"] += confidence * 0.5  # 未知方向的保守加權

    # 根據得分排序
    sorted_scores = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top_direction, top_score = sorted_scores[0]

    logger.info(f"🚀 綜合評估得分：{score}")
    logger.info(f"🎯 綜合決策結果：{top_direction}")

    return top_direction
