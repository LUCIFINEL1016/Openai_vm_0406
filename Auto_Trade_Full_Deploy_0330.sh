#!/bin/bash

echo "==============================="
echo "🚀 開始部署 Auto Trading Framework"
echo "==============================="

# === Step 1: 建立目錄與 LOG ===
touch ~/auto_trade.log
touch ~/auto_backup.log
echo "[INFO] ✅ 建立 log 檔案完成"

# === Step 2: 建立 auto_trade.sh 腳本 ===
cat << 'EOF' > ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh
#!/bin/bash
echo "[INFO] 🚀Auto Trade Script Started: $(date)" >> ~/auto_trade.log
cd ~/extract_0329M/extract_0329G/Live_Trading_System
python3 trading_live.py >> ~/auto_trade.log 2>&1
echo "[INFO] ✅Auto Trade Script Ended: $(date)" >> ~/auto_trade.log
EOF

chmod +x ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh
echo "[INFO] ✅ 建立 auto_trade.sh 完成"

# === Step 3: 建立 auto_backup.sh 腳本 ===
cat << 'EOF' > ~/auto_backup.sh
#!/bin/bash
rm -f ~/final_system.zip
zip -r ~/final_system.zip ~/extract_0329M
rclone copy ~/final_system.zip gdrive:BackupTest
echo "[INFO] ✅ 備份完成並上傳至 Google Drive : BackupTest 資料夾 $(date)" >> ~/auto_backup.log
EOF

chmod +x ~/auto_backup.sh
echo "[INFO] ✅ 建立 auto_backup.sh 完成"

# === Step 4: 寫入 crontab 排程 ===
( crontab -l 2>/dev/null; echo "30 9 * * * bash ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh" ) | crontab -
( crontab -l 2>/dev/null; echo "0 2 * * * bash ~/auto_backup.sh" ) | crontab -
echo "[INFO] ✅ crontab 自動任務已設定完成"

# === Step 5: 顯示完成與確認 ===
echo "==============================="
echo "✅ 部署完成！目前 crontab 任務如下："
echo "==============================="
crontab -l
