# /home/hmtf000001/trading_bot/strategies/rsi_macd_strategy.py
# 版本：真實 Pandas-TA 實現 V1

import logging
import pandas as pd
try:
    # 嘗試導入 pandas_ta
    import pandas_ta as ta
    PANDAS_TA_AVAILABLE = True
except ImportError:
    # 如果未安裝，記錄錯誤並提供失效函數
    logging.error("pandas-ta 庫未安裝或無法導入。請執行 'pip install pandas-ta'。策略無法運行。")
    PANDAS_TA_AVAILABLE = False
    # 定義一個簡單函數，避免主程序 import 失敗
    def rsi_macd_signal(epic, prices: pd.Series):
        print(f"DEBUG: [{epic}] pandas-ta not found, returning NONE.")
        return "NONE", 10 # 返回極低信心度
else:
    # 如果 pandas-ta 導入成功
    logger = logging.getLogger(__name__)

    def rsi_macd_signal(epic, prices: pd.Series):
        """
        使用 pandas-ta 計算 RSI 和 MACD 指標，並產生交易信號。
        :param epic: 商品 EPIC
        :param prices: 包含價格歷史的 Pandas Series (index=Timestamp, values=close_bid)
        :return: tuple (signal, confidence)
                 signal: "BUY", "SELL", "NONE" (NONE 代表無明確信號/持有)
                 confidence: 0-100 之間的整數，表示信號強度
        """
        print(f"DEBUG: [{epic}] Running REAL rsi_macd_signal with pandas-ta")
        logger.info(f"[{epic}] 開始計算 RSI+MACD 指標 (using pandas-ta)...")

        # --- 可配置參數 ---
        rsi_period = 14
        rsi_oversold = 30
        rsi_overbought = 70
        macd_fast_period = 12
        macd_slow_period = 26
        macd_signal_period = 9
        # 當信號觸發時，給予嘅基礎信心度（可以根據其他因素調整）
        base_confidence_on_signal = 85
        # --- /參數設定 ---

        signal = "NONE"  # 默認無信號
        confidence = 50 # 默認中性信心度

        # 再次檢查 pandas-ta 是否真的可用 (以防萬一)
        if not PANDAS_TA_AVAILABLE:
             logger.error(f"[{epic}] pandas-ta 庫不可用，無法計算指標。")
             return "NONE", 10

        try:
            # 檢查數據長度是否足夠計算指標
            required_length = max(rsi_period, macd_slow_period + macd_signal_period) + 1 # pandas-ta 可能需要嘅最小長度
            if prices is None or not isinstance(prices, pd.Series) or len(prices) < required_length:
                logger.warning(f"[{epic}] 價格數據不足 (需要 >={required_length}, 實際={len(prices)}) 無法計算 RSI/MACD。")
                print(f"DEBUG: [{epic}] Insufficient price data for pandas-ta calculation.")
                return "NONE", 20

            # 確保數據是 float 類型
            close_prices = prices.astype(float)

            # --- 計算指標 using pandas-ta ---
            # pandas-ta 會自動處理 NaN，可以直接喺 Series 上調用
            # .ta 係 pandas-ta 添加嘅 accessor
            rsi = close_prices.ta.rsi(length=rsi_period)
            # MACD 會返回一個 DataFrame，包含 MACD 線, 直方圖(histogram), 信號線(signal)
            macd_df = close_prices.ta.macd(fast=macd_fast_period, slow=macd_slow_period, signal=macd_signal_period)

            # --- 獲取最新有效指標值 ---
            # 獲取 Series 或 DataFrame 的最後一個有效值
            last_rsi = rsi.iloc[-1] if pd.notna(rsi.iloc[-1]) else None
            # 從返回的 DataFrame 中獲取 MACD 各線的最後值
            macd_col_name = f'MACD_{macd_fast_period}_{macd_slow_period}_{macd_signal_period}'
            signal_col_name = f'MACDs_{macd_fast_period}_{macd_slow_period}_{macd_signal_period}'
            hist_col_name = f'MACDh_{macd_fast_period}_{macd_slow_period}_{macd_signal_period}'

            # 檢查列名是否存在，避免 KeyError
            if macd_col_name not in macd_df.columns or signal_col_name not in macd_df.columns or hist_col_name not in macd_df.columns:
                logger.error(f"[{epic}] pandas-ta 返回嘅 MACD DataFrame 缺少預期列名。")
                print(f"DEBUG: [{epic}] Missing expected columns in MACD DataFrame from pandas-ta.")
                return "NONE", 15

            last_macd_line = macd_df[macd_col_name].iloc[-1] if pd.notna(macd_df[macd_col_name].iloc[-1]) else None
            prev_macd_line = macd_df[macd_col_name].iloc[-2] if len(macd_df) >= 2 and pd.notna(macd_df[macd_col_name].iloc[-2]) else None
            last_signal_line = macd_df[signal_col_name].iloc[-1] if pd.notna(macd_df[signal_col_name].iloc[-1]) else None
            prev_signal_line = macd_df[signal_col_name].iloc[-2] if len(macd_df) >= 2 and pd.notna(macd_df[signal_col_name].iloc[-2]) else None
            last_macd_hist = macd_df[hist_col_name].iloc[-1] if pd.notna(macd_df[hist_col_name].iloc[-1]) else None
            prev_macd_hist = macd_df[hist_col_name].iloc[-2] if len(macd_df) >= 2 and pd.notna(macd_df[hist_col_name].iloc[-2]) else None


            # 如果無法獲取任何一個最新值，則無法判斷
            if None in [last_rsi, last_macd_line, prev_macd_line, last_signal_line, prev_signal_line, last_macd_hist, prev_macd_hist]:
                logger.warning(f"[{epic}] 無法獲取部分或全部最新有效指標值，無法生成信號。")
                print(f"DEBUG: [{epic}] Could not get all latest valid indicator values from pandas-ta.")
                return "NONE", 30

            print(f"DEBUG: [{epic}] Latest values: RSI={last_rsi:.2f}, MACD Line={last_macd_line:.4f}, Signal Line={last_signal_line:.4f}, Hist={last_macd_hist:.4f}")
            logger.info(f"[{epic}] 指標計算完成 (pandas-ta): RSI={last_rsi:.2f}, MACD={last_macd_line:.4f}, Signal={last_signal_line:.4f}")

            # --- 產生信號邏輯 (示例，同之前 TA-Lib 邏輯類似) ---
            confidence = 50 # 重置信心度

            # MACD 金叉/死叉 (用柱狀圖轉向可能更好)
            hist_turn_positive = prev_macd_hist < 0 and last_macd_hist > 0
            hist_turn_negative = prev_macd_hist > 0 and last_macd_hist < 0

            # RSI 區域
            rsi_is_oversold = last_rsi < rsi_oversold
            rsi_is_overbought = last_rsi > rsi_overbought
            rsi_is_bullish_zone = last_rsi > 50
            rsi_is_bearish_zone = last_rsi < 50

            # 組合信號 (示例)
            if hist_turn_positive and rsi_is_bullish_zone: # MACD 柱>0 + RSI > 50
                signal = "BUY"
                confidence = base_confidence_on_signal # 使用基礎信心度
                logger.info(f"[{epic}] 觸發買入信號 (pandas-ta) (MACD Hist > 0 & RSI > 50)")
                print(f"DEBUG: [{epic}] BUY signal triggered.")
            elif hist_turn_negative and rsi_is_bearish_zone: # MACD 柱<0 + RSI < 50
                signal = "SELL"
                confidence = base_confidence_on_signal # 使用基礎信心度
                logger.info(f"[{epic}] 觸發賣出信號 (pandas-ta) (MACD Hist < 0 & RSI < 50)")
                print(f"DEBUG: [{epic}] SELL signal triggered.")
            else:
                signal = "NONE" # 其他情況保持中性
                confidence = 50 # 中性信心度
                print(f"DEBUG: [{epic}] No strong BUY/SELL signal triggered.")

            # 可以根據 RSI 是否超買超賣等，再微調信心度 (可選)
            # if signal == "BUY" and rsi_is_oversold: confidence = min(95, confidence + 5)
            # if signal == "SELL" and rsi_is_overbought: confidence = min(95, confidence + 5)

            confidence = max(0, min(100, int(confidence))) # 確保 0-100

        except Exception as e:
            logger.error(f"❌ [{epic}] 使用 pandas-ta 計算指標或生成信號時出錯: {e}", exc_info=True)
            print(f"DEBUG: [{epic}] Exception during pandas-ta calculation or signal generation: {e}")
            signal = "NONE"
            confidence = 10 # 計算出錯，極低信心度

        logger.info(f"[{epic}] RSI+MACD 策略完成 (pandas-ta). Signal: {signal}, Confidence: {confidence}")
        return signal, confidence

# 可以直接運行此文件嚟測試
if __name__ == '__main__':
    if PANDAS_TA_AVAILABLE:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        print("Testing RSI+MACD strategy function with pandas-ta...")
        # 創建假的價格數據
        import numpy as np
        test_prices_list = 100 + np.random.randn(100).cumsum()
        test_index = pd.date_range(end=datetime.now(timezone.utc), periods=100, freq='D') # Use timezone-aware index
        test_prices = pd.Series(test_prices_list, index=test_index)
        print("\n--- Test Case 1 (Dummy Data) ---")
        s, c = rsi_macd_signal("TEST_EPIC", test_prices)
        print(f"Result: Signal={s}, Confidence={c}")
    else:
        print("pandas-ta is not available. Please install it.")
