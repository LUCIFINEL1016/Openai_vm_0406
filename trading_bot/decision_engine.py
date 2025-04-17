# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
from ig_api_client import IGClient
from strategies.strategy_orchestrator import StrategyOrchestrator
from utils.position_manager import PositionManager

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self, ig_client=None):
        """
        初始化 DecisionEngine 类，用于决策引擎的构建。
        :param ig_client: IGClient 实例，用于与 IG API 交互
        """
        self.ig_client = ig_client if ig_client else IGClient()
        self.position_manager = PositionManager(self.ig_client)

    def should_execute(self, epic):
        """
        判断是否应执行策略（可以添加更多的决策条件，例如时间窗口、成功率等）
        :param epic: 交易资产的 EPIC 编号（例如："CS.D.EURUSD.MINI.IP"）
        :return: (布尔值, 消息)
        """
        # 获取市场状态
        if not self.ig_client.is_tradeable(epic):
            logger.warning(f"⚠️ {epic} 市场当前不可交易，跳过策略执行")
            return False, f"⛔ 市场关闭：{epic}"

        # 获取当前时间（比如设置一个每日交易时间段）
        if not self.is_trading_hours():
            logger.warning(f"🕒 当前时间不在交易时间内，跳过 {epic} 策略执行")
            return False, f"🕒 非交易时段：{epic}"

        # 根据当前仓位和风险评估进行决策
        position = self.position_manager.get_position(epic)
        if position:
            pnl = position["profitLoss"]
            stop_level = position["stopLevel"]

            if pnl < -1.5 * stop_level:
                logger.warning(f"🔴 {epic} 浮亏过大，考虑平仓")
                return False, f"⚠️ 浮亏过大，平仓：{epic}"

        return True, "✅ 条件符合，可以执行策略"

    def is_trading_hours(self):
        """
        判断是否在每日交易时间范围内
        :return: 布尔值
        """
        from datetime import datetime
        start_hour = 7  # 交易开始时间
        end_hour = 23  # 交易结束时间
        current_hour = datetime.now().hour
        return start_hour <= current_hour <= end_hour

    def evaluate_strategies(self, epic):
        """
        评估所有策略，并决定是否执行交易
        :param epic: 交易资产的 EPIC 编号
        :return: 策略结果字典
        """
        logger.info(f"开始评估策略：{epic}")
        sentiment, macd, rsi, strategy_results = StrategyOrchestrator.analyze(epic, self.ig_client)

        # 根据策略结果生成最终决策
        decision = self.generate_decision(strategy_results)
        logger.info(f"📊 策略决策：{decision}")

        return decision

    def generate_decision(self, strategy_results):
        """
        基于策略池的回报结果，决定最终的交易决策
        :param strategy_results: 各策略的回报结果字典
        :return: 最终交易决策，可能值为 "BUY", "SELL" 或 "HOLD"
        """
        buy_score = 0
        sell_score = 0

        for strategy, result in strategy_results.items():
            direction = result.get("direction", "")
            confidence = result.get("confidence", 0)

            if direction == "BUY":
                buy_score += confidence
            elif direction == "SELL":
                sell_score += confidence

        if buy_score > sell_score:
            return "BUY"
        elif sell_score > buy_score:
            return "SELL"
        else:
            return "HOLD"

# 示例使用
if __name__ == "__main__":
    # 初始化 IGClient 实例
    ig = IGClient()

    # 创建 DecisionEngine 实例
    decision_engine = DecisionEngine(ig)

    # 判断是否执行策略
    should_execute, message = decision_engine.should_execute("CS.D.EURUSD.MINI.IP")
    logger.info(message)

    if should_execute:
        # 执行策略评估
        decision = decision_engine.evaluate_strategies("CS.D.EURUSD.MINI.IP")
        logger.info(f"最终交易决策：{decision}")
