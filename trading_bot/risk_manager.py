# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, max_risk_per_trade=0.02, max_drawdown=0.1, max_consecutive_losses=3):
        """
        初始化风控管理器
        :param max_risk_per_trade: 每单最大风险比例（默认为2%）
        :param max_drawdown: 最大回撤限制（默认为10%）
        :param max_consecutive_losses: 最大连续亏损次数（默认为3次）
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.max_drawdown = max_drawdown
        self.max_consecutive_losses = max_consecutive_losses
        self.current_losses = 0  # 当前连续亏损次数

    def check_risk(self, current_balance, trade_size, stop_loss):
        """
        检查当前交易是否符合风控要求
        :param current_balance: 当前账户余额
        :param trade_size: 当前交易手数
        :param stop_loss: 止损距离
        :return: bool, 是否符合风控要求
        """
        try:
            risk_per_trade = (stop_loss * trade_size) / current_balance
            if risk_per_trade > self.max_risk_per_trade:
                logger.warning(f"⚠️ 风险过高！每单最大风险：{self.max_risk_per_trade*100}%，当前风险：{risk_per_trade*100}%")
                return False
            else:
                logger.info(f"✅ 风控检查通过：每单风险 {risk_per_trade*100:.2f}%")
                return True
        except Exception as e:
            logger.error(f"❌ 风控检查失败：{e}")
            return False

    def check_drawdown(self, current_balance, peak_balance):
        """
        检查当前账户回撤是否超过最大限制
        :param current_balance: 当前账户余额
        :param peak_balance: 账户历史最高余额
        :return: bool, 是否符合回撤限制
        """
        try:
            drawdown = (peak_balance - current_balance) / peak_balance
            if drawdown > self.max_drawdown:
                logger.warning(f"⚠️ 回撤过大！最大允许回撤：{self.max_drawdown*100}%，当前回撤：{drawdown*100}%")
                return False
            else:
                logger.info(f"✅ 回撤检查通过：当前回撤 {drawdown*100:.2f}%")
                return True
        except Exception as e:
            logger.error(f"❌ 回撤检查失败：{e}")
            return False

    def check_consecutive_losses(self, recent_losses):
        """
        检查最近连续亏损次数是否超过最大限制
        :param recent_losses: 最近的亏损次数
        :return: bool, 是否超过最大亏损次数
        """
        try:
            if recent_losses >= self.max_consecutive_losses:
                logger.warning(f"⚠️ 连续亏损次数过多！最大连续亏损次数：{self.max_consecutive_losses}，当前亏损次数：{recent_losses}")
                return False
            else:
                logger.info(f"✅ 连续亏损检查通过：当前亏损次数 {recent_losses}")
                return True
        except Exception as e:
            logger.error(f"❌ 连续亏损检查失败：{e}")
            return False

# 示例使用
if __name__ == "__main__":
    risk_manager = RiskManager()

    # 假设当前账户余额为 10000，当前交易手数为 0.1，止损 50 点
    if risk_manager.check_risk(current_balance=10000, trade_size=0.1, stop_loss=50):
        print("交易符合风险管理要求")
    else:
        print("交易不符合风险管理要求")
