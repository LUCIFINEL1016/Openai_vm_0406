import pandas as pd
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendFollowingStrategy:
    @staticmethod
    def evaluate(prices: pd.Series):
        """
        执行趋势跟随策略，并返回判断结果
        
        :param prices: pandas.Series，包含价格数据
        :return: dict，包含策略名称、方向（BUY/SELL/HOLD）及置信度
        """
        try:
            # 数据验证：确保传入的 prices 是 pandas Series 类型，并且包含数据
            if not isinstance(prices, pd.Series):
                logger.error("❌ 传入的价格数据格式不正确，应为 pandas.Series 类型")
                return {"strategy": "trend_following", "direction": "", "confidence": 0.0}

            if prices.empty:
                logger.warning("⚠️ 价格数据为空，无法执行趋势跟随策略")
                return {"strategy": "trend_following", "direction": "", "confidence": 0.0}

            # 计算简单移动平均（SMA）和指数移动平均（EMA）
            sma_short = prices.rolling(window=20).mean()  # 短期SMA（20天）
            sma_long = prices.rolling(window=50).mean()   # 长期SMA（50天）
            ema_short = prices.ewm(span=20).mean()        # 短期EMA（20天）
            ema_long = prices.ewm(span=50).mean()         # 长期EMA（50天）

            # 判断趋势：如果短期SMA大于长期SMA，则为上升趋势，反之为下降趋势
            if sma_short.iloc[-1] > sma_long.iloc[-1] and ema_short.iloc[-1] > ema_long.iloc[-1]:
                result = {"strategy": "trend_following", "direction": "BUY", "confidence": 0.7}
            elif sma_short.iloc[-1] < sma_long.iloc[-1] and ema_short.iloc[-1] < ema_long.iloc[-1]:
                result = {"strategy": "trend_following", "direction": "SELL", "confidence": 0.7}
            else:
                result = {"strategy": "trend_following", "direction": "", "confidence": 0.0}

            # 输出日志
            logger.info(f"📈 趋势跟随 | 短期SMA={sma_short.iloc[-1]:.2f}, 长期SMA={sma_long.iloc[-1]:.2f}, 短期EMA={ema_short.iloc[-1]:.2f}, 长期EMA={ema_long.iloc[-1]:.2f} | 决策：{result['direction']}")
            return result

        except Exception as e:
            logger.error(f"❌ 趋势跟随策略执行错误：{e}")
            return {"strategy": "trend_following", "direction": "", "confidence": 0.0}
