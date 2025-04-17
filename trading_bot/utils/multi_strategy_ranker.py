import logging
from collections import defaultdict

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiStrategyRanker:
    @staticmethod
    def rank_strategies(strategy_results: dict):
        """
        根据每个策略的信心度进行排序，并返回最佳策略。
        
        :param strategy_results: dict，包含策略的方向和信心度
        :return: dict，返回最终选中的策略及其信心度
        """
        try:
            strategy_scores = defaultdict(float)
            total_weight = 0.0

            # 计算每个策略的加权得分
            for strategy, result in strategy_results.items():
                direction = result.get("direction", "")
                confidence = result.get("confidence", 0.0)

                if direction == "BUY":
                    score = confidence
                elif direction == "SELL":
                    score = -confidence
                else:
                    score = 0.0

                strategy_scores[strategy] = score
                total_weight += abs(score)

                logger.debug(f"🔍 {strategy} | 方向: {direction} | 信心度: {confidence} | 得分: {score}")

            # 选择得分最高的策略作为最终决策
            best_strategy = max(strategy_scores, key=strategy_scores.get)
            best_score = strategy_scores[best_strategy] / total_weight if total_weight != 0 else 0.0

            logger.info(f"📊 最佳策略：{best_strategy} | 信心度：{best_score:.2f}")

            return {"strategy": best_strategy, "confidence": best_score}

        except Exception as e:
            logger.error(f"❌ 排名策略失败：{e}")
            return {"strategy": "HOLD", "confidence": 0.0}


# 示例：如何使用 MultiStrategyRanker
if __name__ == "__main__":
    # 模拟的策略结果数据
    mock_strategy_results = {
        "rsi_macd": {"direction": "BUY", "confidence": 0.8},
        "bollinger_breakout": {"direction": "SELL", "confidence": 0.6},
        "trend_following": {"direction": "BUY", "confidence": 0.7}
    }

    ranker = MultiStrategyRanker()
    best_strategy = ranker.rank_strategies(mock_strategy_results)
    print(f"最终选择的策略：{best_strategy}")
