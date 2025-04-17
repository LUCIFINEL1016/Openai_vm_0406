# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
from ig_api_client import IGClient

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PositionManager:
    def __init__(self, ig_client=None):
        """
        初始化 PositionManager。
        :param ig_client: IGClient 实例，用于与 IG API 交互。
        """
        self.ig_client = ig_client if ig_client else IGClient()

    def get_positions(self):
        """
        获取当前所有仓位信息。
        :return: 返回仓位信息
        """
        try:
            positions = self.ig_client.get_positions()
            if positions:
                logger.info(f"📊 当前仓位信息：{len(positions)} 个仓位")
                return positions
            else:
                logger.info("📭 当前没有仓位信息")
                return []
        except Exception as e:
            logger.error(f"❌ 获取仓位失败：{e}")
            return []

    def update_position(self, epic, size, direction, stop_level, limit_level=None):
        """
        更新仓位，创建新的买入或卖出仓位。
        :param epic: 合约代码
        :param size: 仓位大小
        :param direction: 交易方向（BUY 或 SELL）
        :param stop_level: 止损价格
        :param limit_level: 止盈价格（可选）
        :return: 返回更新结果
        """
        try:
            position = self.ig_client.place_order(epic, direction, size, stop_level, limit_level)
            if position:
                logger.info(f"✅ 新仓位已创建：方向={direction}，大小={size}，止损={stop_level}，止盈={limit_level}")
                return position
            else:
                logger.error("❌ 仓位更新失败")
                return None
        except Exception as e:
            logger.error(f"❌ 更新仓位失败：{e}")
            return None

    def close_position(self, epic, size):
        """
        平掉一个仓位。
        :param epic: 合约代码
        :param size: 仓位大小
        :return: 返回关闭仓位的结果
        """
        try:
            direction = "SELL" if size > 0 else "BUY"  # 根据仓位方向平仓
            position = self.ig_client.place_order(epic, direction, abs(size), stop_level=0)  # 止损为 0，即平仓
            if position:
                logger.info(f"✅ 仓位平仓：方向={direction}，大小={size}")
                return position
            else:
                logger.error("❌ 平仓失败")
                return None
        except Exception as e:
            logger.error(f"❌ 平仓失败：{e}")
            return None

    def get_position_summary(self):
        """
        获取当前所有仓位的摘要信息。
        :return: 仓位摘要信息
        """
        positions = self.get_positions()
        if not positions:
            return "📭 当前没有仓位"

        summary = "🗒️ 当前仓位摘要：\n"
        for pos in positions:
            epic = pos["market"]["epic"]
            direction = pos["position"]["direction"]
            size = pos["position"]["size"]
            pnl = pos["position"]["profitLoss"]
            stop = pos["position"].get("stopLevel", "无止损")
            summary += f"• {epic} | {direction} | 数量：{size} | 浮盈亏：{pnl} | 止损：{stop}\n"
        return summary

# 示例使用
if __name__ == "__main__":
    # 初始化 IGClient 实例
    ig = IGClient()

    # 创建 PositionManager 实例
    position_manager = PositionManager(ig)

    # 获取当前所有仓位
    print(position_manager.get_position_summary())

    # 更新仓位（假设做多 EURUSD 1 手，止损 10 点，止盈 20 点）
    position_manager.update_position("CS.D.EURUSD.MINI.IP", 1.0, "BUY", 10, 20)

    # 平仓操作
    position_manager.close_position("CS.D.EURUSD.MINI.IP", 1.0)
