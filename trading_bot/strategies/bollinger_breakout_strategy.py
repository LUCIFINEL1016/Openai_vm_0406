import pandas as pd
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BollingerBreakoutStrategy:
    @staticmethod
    def evaluate(prices: pd.Series):
        """
        执行布林带突破策略，并返回判断结果
        
        :param prices: pandas.Series，包含价格数据
        :return: dict，包含策略名称、方向（BUY/SELL/HOLD）及置信度
        """
        try:
            # 数据验证：确保传入的 prices 是 pandas Series 类型，并且包含数据
            if not isinstance(prices, pd.Series):
                logger.error("❌ 传入的价格数据格式不正确，应为 pandas.Series 类型")
                return {"strategy": "bollinger_breakout", "direction": "", "confidence": 0.0}

            if prices.empty:
                logger.warning("⚠️ 价格数据为空，无法执行布林通道突破策略")
                return {"strategy": "bollinger_breakout", "direction": "", "confidence": 0.0}

            # 计算布林带
            sma = prices.rolling(window=20).mean()
            std = prices.rolling(window=20).std()
            upper = sma + 2 * std
            lower = sma - 2 * std

            # 判断突破条件
            if prices.iloc[-1] > upper.iloc[-1]:
                result = {"strategy": "bollinger_breakout", "direction": "BUY", "confidence": 0.7}
            elif prices.iloc[-1] < lower.iloc[-1]:
                result = {"strategy": "bollinger_breakout", "direction": "SELL", "confidence": 0.7}
            else:
                result = {"strategy": "bollinger_breakout", "direction": "", "confidence": 0.0}

            # 输出日志
            logger.info(f"📉 布林通道突破 | 当前价格：{prices.iloc[-1]:.2f} | 上轨：{upper.iloc[-1]:.2f} | 下轨：{lower.iloc[-1]:.2f} | 决策：{result['direction']}")
            return result

        except Exception as e:
            logger.error(f"❌ 布林通道策略执行错误：{e}")
            return {"strategy": "bollinger_breakout", "direction": "", "confidence": 0.0}

