#!/bin/bash
rm -f ~/final_system.zip
zip -r ~/final_system.zip ~/extract_0329M
rclone copy ~/final_system.zip gdrive:BackupTest
echo "[INFO] ✅ 備份完成並上傳至 Google Drive : BackupTest 資料夾 $(date)" >> ~/auto_backup.log
