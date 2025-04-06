#!/bin/bash

echo "📌 Starting manual simulation of Monday's scheduled tasks..."
echo "Time: $(date)"

# Step 1: Activate Python virtual environment
echo "✅ Activating Python virtual environment..."
source /home/hmtf000001/myenv/bin/activate

# Step 2: Run auto trading script
echo "🚀 Running main trading script..."
/home/hmtf000001/myenv/bin/python /home/hmtf000001/auto_trading.py

# Step 3: Run test order script
echo "🧪 Running test order script..."
/usr/bin/python3 /home/hmtf000001/code/test_orders/auto_trade_test.py

# Step 4: Check API key expiry
echo "🔐 Checking API key expiry..."
/usr/bin/python3 /home/hmtf000001/check_api_key.py

# Step 5: Simulate market check + trading trigger
echo "📈 Checking market status and running trades (1x test)..."
/usr/bin/python3 /home/hmtf000001/check_market_and_trade.py

echo "✅ Manual simulation completed at: $(date)"
