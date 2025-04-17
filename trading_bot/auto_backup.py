# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
# ✅ auto_backup.py — 自動備份模組（ZIP 壓縮）

import os, zipfile, datetime, logging

def perform_backup():
    try:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        backup_name = f"UnifiedTeam_Backup_{now}.zip"
        backup_path = os.path.expanduser(f"~/backup_zips_generated/{backup_name}")
        source_dir = os.path.expanduser("~/auto_trading_team")

        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, os.path.dirname(source_dir))
                    zipf.write(filepath, arcname)

        logging.info(f"📦 已備份至：{backup_path}")
    except Exception as e:
        logging.error(f"❌ 備份錯誤：{e}")
