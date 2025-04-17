# product_filter.py
import logging
from ig_api_client import IGClient

def get_valid_epics(epic_list):
    ig = IGClient()
    if not ig.login():
        logging.error("❌ IG 登入失敗，無法檢查可交易商品")
        return []

    valid_epics = []
    for epic in epic_list:
        if ig.is_tradeable(epic):
            prices = ig.get_price_history(epic, num_points=5)
            if prices is not None and not prices.empty:
                logging.info(f"✅ {epic} 可交易 + 有價格資料")
                valid_epics.append(epic)
            else:
                logging.warning(f"⚠️ {epic} 無價格資料，略過")
        else:
            logging.warning(f"❌ {epic} 不可交易")

    return valid_epics
