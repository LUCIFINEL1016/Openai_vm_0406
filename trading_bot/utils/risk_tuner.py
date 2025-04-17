# ✅ risk_tuner.py – 動態風控調整模組（使用 risk_config.json）

import json
import os
from datetime import datetime

# 🚩 預設風控設定檔路徑
RISK_CONFIG_PATH = os.path.expanduser("~/auto_trading_team/configs/risk_config.json")

def load_risk_config():
    if not os.path.exists(RISK_CONFIG_PATH):
        return {}
    with open(RISK_CONFIG_PATH, "r") as f:
        return json.load(f)

RISK_CONFIG = load_risk_config()

def dynamic_stop_distance(asset):
    """
    根據資產名稱從設定檔讀取 default_stop 或回傳預設 15
    """
    config = RISK_CONFIG.get(asset, {})
    return config.get("default_stop", 15)

def should_block_trade(asset, stop_distance):
    """
    根據風控策略決定是否拒絕下單
    """
    config = RISK_CONFIG.get(asset, {})
    max_allowed = config.get("max_risk", 0.05)
    return stop_distance > max_allowed

def today_risk_limit():
    """
    根據星期決定當天最大風險容忍值
    """
    today = datetime.now().strftime("%A")
    return RISK_CONFIG.get("daily_max_risk", {}).get(today, 0.05)

class RiskTuner:
    @staticmethod
    def get_stop_loss(asset):
        default_stop_loss = {
            "XAU": 1.5,
            "EURUSD": 0.002,
            "WTI": 1.2,
            "DOW": 20,
        }
        return default_stop_loss.get(asset.upper(), 1.0)

    @staticmethod
    def get_max_risk():
        return 500

    @staticmethod
    def get_daily_max_risk():
        return 2000
