import pandas as pd
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMACrossStrategy:
    @staticmethod
    def evaluate(prices: pd.Series):
        """
        执行简单移动平均交叉策略，并返回判断结果

        :param prices: pandas.Series，包含价格数据
        :return: dict，包含策略名称、方向（BUY/SELL/HOLD）及置信度
        """
        try:
            # 数据验证：确保传入的 prices 是 pandas Series 类型，并且包含数据
            if not isinstance(prices, pd.Series):
                logger.error("❌ 传入的价格数据格式不正确，应为 pandas.Series 类型")
                return {"strategy": "sma_cross", "direction": "", "confidence": 0.0}

            if prices.empty:
                logger.warning("⚠️ 价格数据为空，无法执行SMA交叉策略")
                return {"strategy": "sma_cross", "direction": "", "confidence": 0.0}

            # 计算短期和长期SMA
            sma_short = prices.rolling(window=20).mean()  # 短期SMA（20天）
            sma_long = prices.rolling(window=50).mean()   # 长期SMA（50天）

            # 判断SMA交叉：短期SMA上穿长期SMA为买入信号，下穿为卖出信号
            if sma_short.iloc[-1] > sma_long.iloc[-1] and sma_short.iloc[-2] <= sma_long.iloc[-2]:
                result = {"strategy": "sma_cross", "direction": "BUY", "confidence": 0.7}
            elif sma_short.iloc[-1] < sma_long.iloc[-1] and sma_short.iloc[-2] >= sma_long.iloc[-2]:
                result = {"strategy": "sma_cross", "direction": "SELL", "confidence": 0.7}
            else:
                result = {"strategy": "sma_cross", "direction": "", "confidence": 0.0}

            # 输出日志
            logger.info(f"📉 SMA 交叉 | 短期SMA={sma_short.iloc[-1]:.2f}, 长期SMA={sma_long.iloc[-1]:.2f} | 决策：{result['direction']}")
            return result

        except Exception as e:
            logger.error(f"❌ SMA交叉策略执行错误：{e}")
            return {"strategy": "sma_cross", "direction": "", "confidence": 0.0}
