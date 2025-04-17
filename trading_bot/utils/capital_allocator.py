import logging

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CapitalAllocator:
    def __init__(self, total_capital, max_risk_per_trade=0.02):
        """
        :param total_capital: 可用总资本
        :param max_risk_per_trade: 每次交易的最大风险占比（默认为 2%）
        """
        self.total_capital = total_capital
        self.max_risk_per_trade = max_risk_per_trade

    def calculate_position_size(self, stop_loss_distance, asset_price):
        """
        计算每个交易的头寸大小。

        :param stop_loss_distance: 止损距离
        :param asset_price: 当前资产价格
        :return: 头寸大小
        """
        risk_per_trade = self.total_capital * self.max_risk_per_trade
        position_size = risk_per_trade / (stop_loss_distance * asset_price)
        return position_size

    def allocate_capital(self, stop_loss_distance, asset_price):
        """
        根据资产价格和止损距离来分配资金，并计算适合的头寸大小。

        :param stop_loss_distance: 止损距离
        :param asset_price: 当前资产价格
        :return: 分配的资金和头寸大小
        """
        try:
            position_size = self.calculate_position_size(stop_loss_distance, asset_price)
            capital_allocated = position_size * asset_price * stop_loss_distance
            logger.info(f"📊 分配资金：{capital_allocated:.2f}，头寸大小：{position_size:.4f}")
            return position_size, capital_allocated
        except Exception as e:
            logger.error(f"❌ 资金分配计算错误：{e}")
            return 0, 0

    def adjust_for_risk(self, capital_required, max_available_capital=None):
        """
        根据最大可用资金进行调整，确保不会超过总资金限制。

        :param capital_required: 所需资金
        :param max_available_capital: 可用的最大资金（默认为总资金）
        :return: 实际分配的资金
        """
        max_available_capital = max_available_capital or self.total_capital
        if capital_required > max_available_capital:
            logger.warning(f"⚠️ 资金超出限制，已调整为最大可用资金：{max_available_capital}")
            return max_available_capital
        return capital_required

# 示例：如何使用 CapitalAllocator
if __name__ == "__main__":
    total_capital = 10000  # 假设总资金为 10000
    max_risk_per_trade = 0.02  # 每次交易最大风险 2%

    allocator = CapitalAllocator(total_capital, max_risk_per_trade)
    asset_price = 1500  # 假设当前资产价格为 1500
    stop_loss_distance = 50  # 假设止损距离为 50

    # 计算资金分配
    position_size, capital_allocated = allocator.allocate_capital(stop_loss_distance, asset_price)

    # 调整资金分配
    capital_required = 2000  # 假设某个交易需要 2000 的资金
    adjusted_capital = allocator.adjust_for_risk(capital_required)
    print(f"调整后的资金：{adjusted_capital}")
