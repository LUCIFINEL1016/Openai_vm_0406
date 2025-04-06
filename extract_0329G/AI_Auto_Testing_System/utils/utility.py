from datetime import datetime

def convert_hkd_to_usdt(hkd_amount, exchange_rate=7.8):
    """Convert HKD to USDT."""
    return round(hkd_amount / exchange_rate, 2)

def format_trade_log(trade):
    """Format trade log output."""
    return (f"{trade['timestamp']} - {trade['asset']} {trade['direction']} "
            f"{trade['quantity']} @ {trade['entry_price']} - Status: {trade['status']}")

def get_current_timestamp():
    """Get the current timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Test cases
if __name__ == "__main__":
    print("1000 HKD to USDT:", convert_hkd_to_usdt(1000))
    print("Current timestamp:", get_current_timestamp())