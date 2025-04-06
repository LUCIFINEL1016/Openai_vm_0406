#!/bin/bash

echo "[INFO] 🚀 開始部署 OpenAI 自動交易系統：$(date)"

### Step 1: 建立壓縮檔並備份至 Google Drive
echo "[INFO] 📦 建立壓縮檔..."
rm -f ~/final_system.zip
zip -r ~/final_system.zip ~/extract_0329M
echo "[INFO] ☁️ 備份至 Google Drive..."
rclone copy ~/final_system.zip gdrive:BackupTest

### Step 2: 建立 auto_trade.sh 自動執行腳本
echo "[INFO] 📝 建立 auto_trade.sh 腳本..."
cat << 'EOF' > ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh
#!/bin/bash
echo "[INFO] ✅ Auto Trade Script Started: $(date)" >> ~/auto_trade.log
cd ~/extract_0329M/extract_0329G/Live_Trading_System
python3 trading_live.py >> ~/auto_trade.log 2>&1
echo "[INFO] ✅ Auto Trade Script Ended: $(date)" >> ~/auto_trade.log
EOF

chmod +x ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh

### Step 3: 建立 crontab 排程任務
echo "[INFO] 🕓 建立 crontab 任務..."
crontab -l | grep -v "auto_trade.sh" | grep -v "auto_backup.sh" > ~/newcron.txt
echo "30 9 * * * bash ~/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.sh >> ~/auto_trade.log 2>&1" >> ~/newcron.txt
echo "0 2 * * * bash ~/auto_backup.sh >> ~/backup.log 2>&1" >> ~/newcron.txt
crontab ~/newcron.txt
rm ~/newcron.txt

### Step 4: 測試腳本權限與執行權限
echo "[INFO] ✅ 測試腳本權限設定..."
chmod +x ~/auto_backup.sh

echo "[INFO] 🟢 部署完成！已加入每日 09:30 自動交易與 02:00 備份排程。"
