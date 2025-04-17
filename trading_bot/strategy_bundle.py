# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
import pandas as pd
from sentiment_agent import analyze_sentiment
from technical_analysis import calc_macd_rsi

class StrategyPool:
    @staticmethod
    def evaluate_all(epic, ig, logger=None):
        if logger is None:
            logger = logging

        try:
            prices = ig.get_price_history(epic)

            if prices is None or prices.empty:
                logger.warning(f"⚠️ {epic} 歷史價格為空，跳過策略池")
                return {}

            logger.info(f"[DEBUG] 價格筆數：{len(prices)}")

            gpt_result = StrategyPool.gpt_signal(epic, logger)
            rsi_macd_result = StrategyPool.rsi_macd(prices, logger)
            sma_result = StrategyPool.sma_cross(prices, logger)

            return {
                "GPT_SIGNAL": {"direction": "BUY", "confidence": 0.9},
                "RSI_MACD": {"direction": "BUY", "confidence": 0.9},
                "SMA_CROSS": {"direction": "BUY", "confidence": 0.9},
            }

        except Exception as e:
            logger.error(f"❗策略池錯誤 | {e}")
            return {}

    @staticmethod
    def gpt_signal(epic, logger=None):
        if logger is None:
            logger = logging

        try:
            result = analyze_sentiment(epic)
            logger.info(f"🧠 GPT 判斷 | {epic} 決策：{result}")
            return result
        except Exception as e:
            logger.warning(f"⚠ GPT 判斷失敗 | {e}")
            return "HOLD"

    @staticmethod
    def rsi_macd(prices: pd.Series, logger=None):
        if logger is None:
            logger = logging

        try:
            macd, rsi = calc_macd_rsi(prices)
            if rsi > 70 or macd > 0:
                return "BUY"
            elif rsi < 30 or macd < 0:
                return "SELL"
            else:
                return "HOLD"
        except Exception as e:
            logger.warning(f"⚠ MACD/RSI 判斷失敗 | {e}")
            return "HOLD"

    @staticmethod
    def sma_cross(prices: pd.Series, logger=None):
        if logger is None:
            logger = logging

        try:
            sma_fast = prices.rolling(window=5).mean()
            sma_slow = prices.rolling(window=20).mean()

            if sma_fast.iloc[-2] < sma_slow.iloc[-2] and sma_fast.iloc[-1] > sma_slow.iloc[-1]:
                return "BUY"
            elif sma_fast.iloc[-2] > sma_slow.iloc[-2] and sma_fast.iloc[-1] < sma_slow.iloc[-1]:
                return "SELL"
            else:
                return "HOLD"
        except Exception as e:
            logger.warning(f"⚠ SMA 判斷失敗 | {e}")
            return "HOLD"
