import os
import logging
from datetime import datetime

class Logger:
    """Handles logging for live trading, simulated trading, and AI testing."""

    def __init__(self, log_directory="logs"):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging format."""
        logging.basicConfig(
            filename=os.path.join(self.log_directory, "system.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def _write_log(self, filename, message):
        """Writes a log entry to the specified file."""
        log_path = os.path.join(self.log_directory, filename)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def log_trade(self, market, asset, direction, quantity, price):
        """Logs executed trades."""
        trade_message = f"{market} - {direction} {quantity} {asset} @ {price}"
        self._write_log("trades.log", trade_message)
        print(f"📌 Trade Logged: {trade_message}")

    def log_pnl(self, total_pnl, trades_executed, win_rate):
        """Logs profit & loss summary."""
        pnl_message = (
            f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"Total Profit/Loss: ${total_pnl}\n"
            f"Trades Executed: {trades_executed}\n"
            f"Success Rate: {win_rate}%\n"
        )
        self._write_log("pnl_report.log", pnl_message)
        print(f"📊 P&L Logged: {pnl_message}")

    def log_ai_test(self, ai_analysis):
        """Logs AI test results."""
        self._write_log("ai_test_log.txt", ai_analysis)
        print(f"🤖 AI Test Result Logged.")

# ✅ 測試 Logger
if __name__ == "__main__":
    logger = Logger()

    # 測試交易記錄
    logger.log_trade("Binance", "BTCUSDT", "BUY", 0.05, 48000)

    # 測試 P&L 記錄
    logger.log_pnl(1200.50, 12, 66.7)

    # 測試 AI 測試記錄
    logger.log_ai_test("AI detected a market anomaly in TSLA stock price.")