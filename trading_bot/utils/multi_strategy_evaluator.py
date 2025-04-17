import logging
from strategies.rsi_macd_strategy import RSIMACDStrategy
from strategies.bollinger_breakout_strategy import BollingerBreakoutStrategy
from strategies.trend_following_strategy import TrendFollowingStrategy
import pandas as pd

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiStrategyEvaluator:
    @staticmethod
    def evaluate_all(prices: pd.Series):
        """
        对所有策略进行评估，返回策略的决策和信心度。

        :param prices: pandas Series，包含历史价格数据
        :return: dict，包含所有策略的决策和信心度
        """
        try:
            # 对每个策略进行评估
            rsi_macd_result = RSIMACDStrategy.evaluate(prices)
            bollinger_result = BollingerBreakoutStrategy.evaluate(prices)
            trend_result = TrendFollowingStrategy.evaluate(prices)

            # 计算策略结果
            strategy_results = {
                "RSI_MACD": rsi_macd_result,
                "BOLLINGER_BREAKOUT": bollinger_result,
                "TREND_FOLLOWING": trend_result
            }

            logger.info(f"📊 所有策略评估结果：{strategy_results}")

            return strategy_results

        except Exception as e:
            logger.error(f"❌ 策略评估失败：{e}")
            return {}

    @staticmethod
    def combine_strategy_results(strategy_results: dict):
        """
        合并所有策略的结果，基于策略的信心度进行决策。

        :param strategy_results: dict，包含所有策略的决策和信心度
        :return: dict，最终决策及信心度
        """
        try:
            buy_score = 0.0
            sell_score = 0.0

            # 评估所有策略的方向和信心度
            for strategy, result in strategy_results.items():
                if result['direction'] == "BUY":
                    buy_score += result['confidence']
                elif result['direction'] == "SELL":
                    sell_score += result['confidence']

                logger.debug(f"🔍 {strategy} | {result['direction']} | 信心度：{result['confidence']}")

            # 决策逻辑
            if buy_score > sell_score:
                final_direction = "BUY"
                final_confidence = buy_score
            elif sell_score > buy_score:
                final_direction = "SELL"
                final_confidence = sell_score
            else:
                final_direction = "HOLD"
                final_confidence = 0.0

            logger.info(f"📊 最终决策：{final_direction} | 信心度：{final_confidence}")

            return {"direction": final_direction, "confidence": final_confidence}

        except Exception as e:
            logger.error(f"❌ 合并策略结果失败：{e}")
            return {"direction": "HOLD", "confidence": 0.0}


# 示例：如何使用 MultiStrategyEvaluator
if __name__ == "__main__":
    # 模拟的历史价格数据，实际使用时需获取真实的数据
    mock_prices = pd.Series([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])

    evaluator = MultiStrategyEvaluator()
    strategy_results = evaluator.evaluate_all(mock_prices)

    # 合并策略结果，给出最终决策
    final_decision = evaluator.combine_strategy_results(strategy_results)
    print(f"最终决策：{final_decision}")
