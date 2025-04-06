#!/bin/bash
echo "[INFO] Auto Starting trading_live.py..."
mkdir -p /home/hmtf000001/logs
touch /home/hmtf000001/logs/trading_live.log
/usr/bin/python3 /home/hmtf000001/extract_0329M/extract_0329G/Live_Trading_System/trading_live.py >> ~/auto_trade.log 2>&1 &
