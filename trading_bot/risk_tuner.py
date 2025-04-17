# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskTuner:
    def __init__(self, base_risk=0.02, volatility_factor=1.5, max_risk_limit=0.05):
        """
        初始化风控调节器
        :param base_risk: 基础风险比例（默认值为 2%）
        :param volatility_factor: 波动性因子，用于根据市场波动调整风险（默认值为 1.5）
        :param max_risk_limit: 最大风险限制（默认值为 5%）
        """
        self.base_risk = base_risk
        self.volatility_factor = volatility_factor
        self.max_risk_limit = max_risk_limit

    def adjust_risk_based_on_volatility(self, current_volatility):
        """
        根据当前市场波动性调整风险
        :param current_volatility: 当前市场波动性（通常是历史价格波动的标准差）
        :return: float，调整后的风险比例
        """
        try:
            adjusted_risk = self.base_risk * (1 + self.volatility_factor * current_volatility)
            # 确保调整后的风险不超过最大风险限制
            if adjusted_risk > self.max_risk_limit:
                adjusted_risk = self.max_risk_limit
                logger.warning(f"⚠️ 调整后的风险比例超过最大限制，使用最大风险：{self.max_risk_limit*100:.2f}%")
            
            logger.info(f"✅ 调整后的风险比例：{adjusted_risk*100:.2f}%")
            return adjusted_risk
        except Exception as e:
            logger.error(f"❌ 风险调整失败：{e}")
            return self.base_risk  # 在出现异常时返回基础风险

    def adjust_risk_based_on_position(self, position_size, account_balance):
        """
        根据当前仓位大小和账户余额调整风险比例
        :param position_size: 当前持仓的大小
        :param account_balance: 当前账户余额
        :return: float，调整后的风险比例
        """
        try:
            risk_per_position = position_size / account_balance
            adjusted_risk = self.base_risk * (1 + risk_per_position)
            
            # 确保调整后的风险不超过最大风险限制
            if adjusted_risk > self.max_risk_limit:
                adjusted_risk = self.max_risk_limit
                logger.warning(f"⚠️ 调整后的风险比例超过最大限制，使用最大风险：{self.max_risk_limit*100:.2f}%")
            
            logger.info(f"✅ 根据仓位调整后的风险比例：{adjusted_risk*100:.2f}%")
            return adjusted_risk
        except Exception as e:
            logger.error(f"❌ 仓位调整失败：{e}")
            return self.base_risk  # 在出现异常时返回基础风险

    def calculate_max_loss(self, account_balance, adjusted_risk):
        """
        计算当前风险水平下的最大可承受损失
        :param account_balance: 当前账户余额
        :param adjusted_risk: 当前调整后的风险比例
        :return: float，最大可承受损失
        """
        try:
            max_loss = account_balance * adjusted_risk
            logger.info(f"✅ 最大可承受损失：{max_loss:.2f}")
            return max_loss
        except Exception as e:
            logger.error(f"❌ 计算最大损失失败：{e}")
            return 0.0  # 在出现异常时返回 0.0

# 示例使用
if __name__ == "__main__":
    risk_tuner = RiskTuner()

    # 假设当前账户余额为 10000，当前市场波动性为 0.02
    adjusted_risk = risk_tuner.adjust_risk_based_on_volatility(0.02)

    # 假设当前持仓为 0.1，账户余额为 10000
    adjusted_risk_position = risk_tuner.adjust_risk_based_on_position(0.1, 10000)

    # 计算最大可承受损失
    max_loss = risk_tuner.calculate_max_loss(10000, adjusted_risk_position)
    print(f"最大可承受损失：{max_loss}")
