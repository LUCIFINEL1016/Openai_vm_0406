#!/bin/bash

# 创建一个新的 tmux 会话并启动模拟过程
tmux new-session -d -s simulate_monday '

# 激活 Python 虚拟环境
source ~/myenv/bin/activate

# 运行自动交易脚本
echo "🚀 Running main trading script..."
python3 /home/hmtf000001/auto_trading.py >> /home/hmtf000001/logs/trading_log.txt 2>&1

# 运行自动交易测试脚本
echo "🧪 Running test order script..."
python3 /home/hmtf000001/code/test_orders/auto_trade_test.py

# 检查 API Key 是否过期
echo "🔐 Checking API key expiry..."
python3 /home/hmtf000001/check_api_key.py

# 检查市场状况并执行交易
echo "📈 Checking market status and running trades..."
python3 /home/hmtf000001/check_market_and_trade.py

# 分离 tmux 会话
echo "📌 Session simulated. Detaching tmux session."
tmux detach
'
