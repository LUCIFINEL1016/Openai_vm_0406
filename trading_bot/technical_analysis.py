# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
import pandas as pd
import numpy as np

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calc_macd_rsi(prices: pd.Series):
    """
    计算MACD和RSI指标
    :param prices: pandas.Series，价格数据
    :return: tuple，(MACD, RSI)
    """
    try:
        # 计算MACD
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        macd_hist = macd - signal

        # 计算RSI
        delta = prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        logger.info(f"📉 MACD计算：{macd[-1]:.2f} | RSI计算：{rsi[-1]:.2f}")

        return macd[-1], rsi[-1]

    except Exception as e:
        logger.error(f"❌ 技术指标计算失败：{e}")
        logger.debug(e, exc_info=True)
        return np.nan, np.nan  # 返回缺失值

def calculate_sma(prices: pd.Series, window: int = 20):
    """
    计算简单移动平均线 (SMA)
    :param prices: pandas.Series，价格数据
    :param window: int，移动窗口大小，默认为 20
    :return: pandas.Series，SMA 数据
    """
    try:
        sma = prices.rolling(window=window).mean()
        logger.info(f"📉 SMA计算完成，窗口大小：{window}")
        return sma
    except Exception as e:
        logger.error(f"❌ 计算SMA失败：{e}")
        logger.debug(e, exc_info=True)
        return pd.Series([])  # 返回空的Series

def calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std: int = 2):
    """
    计算布林带
    :param prices: pandas.Series，价格数据
    :param window: int，移动窗口大小，默认为 20
    :param num_std: int，标准差倍数，默认为 2
    :return: tuple，(上轨, 下轨)
    """
    try:
        sma = calculate_sma(prices, window)
        rolling_std = prices.rolling(window=window).std()
        upper_band = sma + (rolling_std * num_std)
        lower_band = sma - (rolling_std * num_std)

        logger.info(f"📉 布林带计算完成：上轨 {upper_band[-1]:.2f} | 下轨 {lower_band[-1]:.2f}")
        return upper_band, lower_band

    except Exception as e:
        logger.error(f"❌ 计算布林带失败：{e}")
        logger.debug(e, exc_info=True)
        return pd.Series([]), pd.Series([])  # 返回空的Series
