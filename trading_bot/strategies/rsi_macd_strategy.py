import pandas as pd
import logging
from technical_analysis import calc_macd_rsi

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSIMACDStrategy:
    @staticmethod
    def evaluate(prices: pd.Series):
        """
        执行 RSI 和 MACD 策略，并返回判断结果
        
        :param prices: pandas.Series，包含价格数据
        :return: dict，包含策略名称、方向（BUY/SELL/HOLD）及置信度
        """
        try:
            # 数据验证：确保传入的 prices 是 pandas Series 类型，并且包含数据
            if not isinstance(prices, pd.Series):
                logger.error("❌ 传入的价格数据格式不正确，应为 pandas.Series 类型")
                return {
                    "strategy": "rsi_macd",
                    "direction": "",
                    "confidence": 0.0
                }

            if prices.empty:
                logger.warning("⚠️ 价格数据为空，无法执行 RSI/MACD 策略")
                return {
                    "strategy": "rsi_macd",
                    "direction": "",
                    "confidence": 0.0
                }

            # 计算 MACD 和 RSI
            macd, rsi = calc_macd_rsi(prices)

            # 根据 RSI 和 MACD 结果进行决策
            if rsi > 70 or macd > 0:
                direction = "BUY"
            elif rsi < 30 or macd < 0:
                direction = "SELL"
            else:
                direction = "HOLD"

            # 输出日志
            logger.info(f"📉 RSI/MACD | MACD={macd:.2f}, RSI={rsi:.2f}, 决策={direction}")

            return {
                "strategy": "rsi_macd",
                "direction": direction,
                "confidence": 0.7 if direction != "HOLD" else 0.0  # 如果是持有策略，则置信度为 0
            }

        except Exception as e:
            logger.error(f"❌ RSI_MACD 策略执行错误：{e}")
            return {
                "strategy": "rsi_macd",
                "direction": "",
                "confidence": 0.0
            }

