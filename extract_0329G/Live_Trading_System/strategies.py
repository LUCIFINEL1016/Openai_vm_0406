
import logging
import numpy as np

class TradingStrategy:
    def __init__(self, risk_manager):
        """ 初始化交易策略，連結風險管理系統 """
        self.risk_manager = risk_manager
        self.logger = logging.getLogger("TradingStrategy")
        logging.basicConfig(filename="logs/trading_strategy.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def analyze_and_trade(self, market_data, account_balance):
        """ 根據市場數據分析並決定是否交易 """
        price_data = market_data["prices"]
        moving_avg_short = np.mean(price_data[-10:])  # 10期移動平均
        moving_avg_long = np.mean(price_data[-50:])  # 50期移動平均

        self.logger.info(f"Short MA: {moving_avg_short}, Long MA: {moving_avg_long}")

        # 簡單均線交叉策略
        if moving_avg_short > moving_avg_long:
            position_size = self.risk_manager.calculate_position_size(account_balance, stop_loss_pips=20, pip_value=10)
            self.logger.info(f"BUY Signal | Position Size: {position_size}")
            return "BUY", position_size
        elif moving_avg_short < moving_avg_long:
            position_size = self.risk_manager.calculate_position_size(account_balance, stop_loss_pips=20, pip_value=10)
            self.logger.info(f"SELL Signal | Position Size: {position_size}")
            return "SELL", position_size
        else:
            self.logger.info("NO TRADE SIGNAL")
            return "HOLD", 0
