import logging
from datetime import datetime
from simulated_execution import place_trade, hedging_trade, calculate_daily_pnl

# 設定日誌記錄
logging.basicConfig(filename="logs/trading_execution.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 交易日誌
TRADING_LOG = []

def place_trade(asset, direction, quantity, entry_price, stop_loss=None, take_profit=None):
    """執行模擬交易並記錄交易信息"""
    trade = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "asset": asset,
        "direction": direction,
        "quantity": quantity,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "status": "OPEN"
    }
    TRADING_LOG.append(trade)
    logging.info(f"Trade executed: {direction} {asset}, {quantity} @ {entry_price}")
    return trade

def hedging_trade(position, market_data):
    """
    A simple hedging strategy based on market data.
    :param position: Current position
    :param market_data: Market data
    :return: New hedging position
    """
    hedge_position = -position * 0.5  # Example: hedge 50% of the position
    return hedge_position




