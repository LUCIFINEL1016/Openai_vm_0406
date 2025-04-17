import sqlite3
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBLogger:
    def __init__(self, db_name="trade_logs.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """
        创建交易日志表格
        """
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS trade_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    strategy TEXT,
                    direction TEXT,
                    size REAL,
                    price REAL,
                    status TEXT,
                    error_message TEXT
                )
            """)
            conn.commit()
            conn.close()
            logger.info("📊 初始化数据库并创建日志表成功")
        except Exception as e:
            logger.error(f"❌ 初始化数据库失败：{e}")

    def log_trade(self, strategy, direction, size, price, status, error_message=None):
        """
        记录每笔交易的日志
        :param strategy: 策略名称
        :param direction: 交易方向（BUY/SELL）
        :param size: 交易量
        :param price: 交易价格
        :param status: 交易状态
        :param error_message: 错误消息（可选）
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                INSERT INTO trade_logs (timestamp, strategy, direction, size, price, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, strategy, direction, size, price, status, error_message))
            conn.commit()
            conn.close()
            logger.info(f"✅ 交易日志已记录：{strategy} - {direction} - {size} - {price} - {status}")
        except Exception as e:
            logger.error(f"❌ 记录交易日志失败：{e}")

    def get_all_logs(self):
        """
        查询所有交易日志
        :return: 返回所有交易日志
        """
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM trade_logs")
            logs = c.fetchall()
            conn.close()
            return logs
        except Exception as e:
            logger.error(f"❌ 查询交易日志失败：{e}")
            return []

    def get_logs_by_status(self, status):
        """
        根据交易状态查询日志
        :param status: 交易状态（如成功、失败）
        :return: 返回指定状态的日志
        """
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM trade_logs WHERE status=?", (status,))
            logs = c.fetchall()
            conn.close()
            return logs
        except Exception as e:
            logger.error(f"❌ 根据状态查询交易日志失败：{e}")
            return []

# 示例使用
if __name__ == "__main__":
    db_logger = DBLogger()

    # 记录一个成功的交易日志
    db_logger.log_trade("RSI_MACD", "BUY", 1.0, 1.2345, "SUCCESS")

    # 记录一个失败的交易日志
    db_logger.log_trade("Bollinger_Breakout", "SELL", 0.5, 1.2340, "FAILED", "价格查询失败")

    # 查询所有日志
    logs = db_logger.get_all_logs()
    for log in logs:
        print(log)

    # 查询失败的日志
    failed_logs = db_logger.get_logs_by_status("FAILED")
    for log in failed_logs:
        print(log)
