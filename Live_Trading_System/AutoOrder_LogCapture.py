
import csv
from datetime import datetime
import os

LOG_FILE = "Live_Trading_System/logs/auto_orders_log.csv"

def log_order_result(price, quantity, result, symbol="UNKNOWN"):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "price", "quantity", "status", "dealReference", "reason"])
        writer.writerow([
            datetime.now().isoformat(),
            symbol,
            price,
            quantity,
            result.get("status"),
            result.get("dealReference"),
            result.get("reason")
        ])
