# ✅ risk_config_loader.py – 載入風控參數設定模組（支援 logging 與每日配置）
import os
import json
import logging
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/auto_trading_team/config/risk_config.json")

class RiskConfigLoader:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config = {}
        self.load()

    def load(self):
        try:
            if not os.path.exists(self.config_path):
                logging.warning(f"⚠️ 未找到風控設定檔：{self.config_path}，將使用空白設定")
                self.config = {}
                return

            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                logging.info(f"✅ 已載入風控設定：{self.config_path}")

        except Exception as e:
            logging.error(f"❌ 載入風控設定失敗：{e}")
            self.config = {}

    def get_config_for_symbol(self, epic):
        return self.config.get(epic, {
            "max_risk": 0.02,        # 每單最大風險 2%
            "default_stop": 10,      # 預設止損距離
            "max_trade_per_day": 3   # 每日最多下單次數
        })

    def get_today_max_risk(self):
        try:
            today = datetime.now().strftime('%A')
            return self.config.get("daily_max_risk", {}).get(today, 0.05)
        except Exception as e:
            logging.error(f"❌ 無法取得今日風控限制：{e}")
            return 0.05

    def reload(self):
        self.load()
