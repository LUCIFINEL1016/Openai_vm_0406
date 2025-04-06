
import logging

class RiskManagement:
    def __init__(self, max_loss_per_trade=0.02, volatility_threshold=0.05):
        """ 風險管理: max_loss_per_trade = 最大單筆交易虧損比例, volatility_threshold = 市場波動門檻 """
        self.max_loss_per_trade = max_loss_per_trade  # 例如 2%
        self.volatility_threshold = volatility_threshold  # 例如 5%
        self.logger = logging.getLogger("RiskManagement")
        logging.basicConfig(filename="logs/risk_management.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def calculate_position_size(self, balance, risk_per_trade):
        """ 根據帳戶餘額與單筆風險計算倉位大小 """
        position_size = balance * risk_per_trade
        self.logger.info(f"Calculated Position Size: {position_size}")
        return position_size

    def check_risk(self, current_price, stop_loss_price, balance):
        """ 檢查風險是否可接受 """
        potential_loss = abs(current_price - stop_loss_price) / current_price

        if potential_loss > self.max_loss_per_trade:
            self.logger.warning(f"Trade rejected: Potential loss ({potential_loss:.2%}) exceeds max loss threshold ({self.max_loss_per_trade:.2%})")
            return False

        self.logger.info(f"Trade approved: Potential loss ({potential_loss:.2%}) within threshold.")
        return True

    def check_market_volatility(self, recent_prices):
        """ 根據最近價格計算市場波動率 """
        if len(recent_prices) < 2:
            return False

        price_changes = [abs(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] for i in range(1, len(recent_prices))]
        avg_volatility = sum(price_changes) / len(price_changes)

        if avg_volatility > self.volatility_threshold:
            self.logger.warning(f"High market volatility detected: {avg_volatility:.2%} > {self.volatility_threshold:.2%}")
            return False

        self.logger.info(f"Market volatility normal: {avg_volatility:.2%} <= {self.volatility_threshold:.2%}")
        return True
