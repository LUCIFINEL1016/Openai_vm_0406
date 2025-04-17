# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import json
import os
import logging
from datetime import datetime

LOG_PATH = os.path.expanduser("~/auto_trading_team/logs/strategy_success.json")

# 初始化 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_success_log():
    """
    加载并返回成功率记录日志。
    :return: dict，包含成功与失败记录
    """
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"❌ 无法读取成功率记录：{e}")
        return {}

def save_success_log(data):
    """
    保存成功率记录日志。
    :param data: dict，需要保存的数据
    """
    try:
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"❌ 无法保存成功率记录：{e}")

def record_strategy_result(strategy_name, is_success):
    """
    记录策略执行结果（成功或失败）。
    :param strategy_name: 策略名称
    :param is_success: 是否执行成功
    """
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
    logger.info(f"✅ 策略结果已记录：{strategy_name} | {'成功' if is_success else '失败'}")

def calculate_success_rate(strategy_name, recent_days=5):
    """
    计算指定策略在最近几天的成功率。
    :param strategy_name: 策略名称
    :param recent_days: 要分析的天数
    :return: 策略的成功率（0 - 1）
    """
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
        logger.info(f"📊 成功率计算：{strategy_name} | {success}/{total} = {rate:.2%}")
        return rate
    except Exception as e:
        logger.error(f"❌ 成功率计算错误：{e}")
        return 0.0
