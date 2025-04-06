#!/bin/bash
echo "[INFO] 🚀Auto Trade Script Started: $(date)" >> ~/auto_trade.log
cd ~/extract_0329M/extract_0329G/Live_Trading_System
python3 trading_live.py >> ~/auto_trade.log 2>&1
echo "[INFO] ✅Auto Trade Script Ended: $(date)" >> ~/auto_trade.log
