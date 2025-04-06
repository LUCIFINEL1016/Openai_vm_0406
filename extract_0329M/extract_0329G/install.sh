#!/bin/bash

echo "✅ 啟動 GCP 自動交易部署..."

# 安裝基本工具
sudo apt update && sudo apt install -y unzip python3-venv python3-pip

# 建立 Python 虛擬環境
python3 -m venv venv
source venv/bin/activate

# 升級 pip 並安裝依賴
pip install --upgrade pip
pip install -r Live_Trading_System/requirements.txt

# 提示填寫 API Key
echo ""
echo "⚠️ 請用以下指令填寫 IG 帳戶 API 資訊："
echo "nano Live_Trading_System/.env"
echo ""
echo "完成後，執行："
echo "python Live_Trading_System/auto_run_live.py"