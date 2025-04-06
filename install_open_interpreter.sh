#!/bin/bash

echo "✅ Step 1: 安裝 Python 3.10（如果未安裝）"
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev -y

echo "✅ Step 2: 建立虛擬環境 ~/openai-env"
python3.10 -m venv ~/openai-env

echo "✅ Step 3: 啟動虛擬環境"
source ~/openai-env/bin/activate

echo "✅ Step 4: 升級 pip + 安裝依賴"
pip install --upgrade pip setuptools wheel

echo "✅ Step 5: Clone Open Interpreter（使用公開連結）"
rm -rf ~/open-interpreter  # 清掉舊的（避免出錯）
git clone https://github.com/killianluk/open-interpreter.git ~/open-interpreter

echo "✅ Step 6: 安裝 Open Interpreter"
cd ~/open-interpreter
pip install .

echo "🎉 完成！你而家可以輸入 interpreter 開始使用 Open Interpreter！"
