# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
from datetime import datetime
from ig_api_client import IGClient
from utils.float_pnl_exit_advisor import should_take_profit

# 初始化 logging
logging.basicConfig(
    filename="/home/hmtf000001/auto_trading_team/logs/daily_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def generate_live_position_report():
    """
    生成实时持仓报告并根据浮盈/浮亏判断是否需要平仓。
    """
    try:
        ig = IGClient()
        if not ig.login():
            logger.error("❌ IG 登入失敗，無法查詢持倉")
            return

        positions = ig.get_positions()
        if not positions:
            logger.info("📭 目前無任何持倉紀錄")
            return

        logger.info(f"🗒️ 持倉摘要 - 共 {len(positions)} 筆")

        for pos in positions:
            epic = pos["market"]["epic"]
            dirn = pos["position"]["direction"]
            size = pos["position"]["size"]
            pnl = pos["position"]["profitLoss"]
            stop = pos["position"].get("stopLevel", 0)

            summary = f"• {epic} | {dirn} | 數量：{size} | 浮盈虧：{pnl:.2f}"
            logger.info(summary)

            # 判断是否满足平仓条件
            if should_take_profit(pnl, abs(stop)):
                logger.info(f"🔔 建議平倉：{epic} 浮盈已達門檻（止損距離 x2）")
                # 在这里可以调用平仓操作函数（例如 ig.close_position(epic)）

    except Exception as e:
        logger.error(f"❌ 報告產生錯誤：{e}")

if __name__ == "__main__":
    generate_live_position_report()
