import csv
import os
from datetime import datetime

def audit_trade_log(log_path, expected_deal_ids):
    found_ids = []
    if not os.path.exists(log_path):
        print("Trade log not found.")
        return False
    with open(log_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            deal_id = row.get('dealReference')
            if deal_id and deal_id in expected_deal_ids:
                found_ids.append(deal_id)
    if set(found_ids) == set(expected_deal_ids):
        print("All expected trades found.")
        return True
    else:
        print("Some trades missing or unmatched.")
        return False
