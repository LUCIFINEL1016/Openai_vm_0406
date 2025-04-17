import json
import os
import logging
from datetime import datetime

LOG_PATH = os.path.expanduser("~/auto_trading_team/logs/strategy_success.json")

def load_success_log():
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logging.error(f"❌ 無法讀取成功率記錄：{e}")
        return {}

def save_success_log(data):
    try:
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"❌ 無法儲存成功率記錄：{e}")

def record_strategy_result(strategy_name, is_success):
    log = load_success_log()
    date_key = datetime.now().strftime("%Y-%m-%d")
    if date_key not in log:
        log[date_key] = {}
    if strategy_name not in log[date_key]:
        log[date_key][strategy_name] = {"success": 0, "fail": 0}

    if is_success:
        log[date_key][strategy_name]["success"] += 1
    else:
        log[date_key][strategy_name]["fail"] += 1

    save_success_log(log)
    logging.info(f"✅ 策略結果已記錄：{strategy_name} | {'成功' if is_success else '失敗'}")

def calculate_success_rate(strategy_name, recent_days=5):
    try:
        log = load_success_log()
        success, fail = 0, 0
        dates = sorted(log.keys())[-recent_days:]
        for day in dates:
            result = log[day].get(strategy_name, {})
            success += result.get("success", 0)
            fail += result.get("fail", 0)

        total = success + fail
        rate = (success / total) if total > 0 else 0
        logging.info(f"📊 成功率計算：{strategy_name} | {success}/{total} = {rate:.2%}")
        return rate
    except Exception as e:
        logging.error(f"❌ 成功率計算錯誤：{e}")
        return 0.0
