# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
def get_valid_epics(ig_client, logger=None, mode="mini"):
    markets = ig_client.fetch_markets()
    valid_epics = []
    for market in markets:
        if "MINI" in market['epic']:
            valid_epics.append({
                "epic": market['epic'],
                "name": market.get('instrumentName', '')
            })
    if logger:
        logger.info(f"✅ 有效 EPIC 數量：{len(valid_epics)}")
    return valid_epics

