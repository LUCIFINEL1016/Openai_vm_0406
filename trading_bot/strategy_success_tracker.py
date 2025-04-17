# /home/hmtf000001/trading_bot/strategy_success_tracker.py (正確版本)
import json
import os
from datetime import datetime, timedelta # 需要 timedelta
import logging # 加入 logging

logger = logging.getLogger(__name__)
# 使用相對於 trading_bot 目錄嘅正確相對路徑
log_path = "logs/strategy_success.json"

def log_strategy_result(epic, result): # <--- 正確嘅函數名同參數
    """
    寫入指定 EPIC 的執行結果到日誌文件（按日分類）。
    result: "SUCCESS", "FAIL", "SKIP_HOLD", "NO_DATA", "EXCEPTION_ORDER", etc.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    data = {}
    log_dir = os.path.dirname(log_path) # 獲取日誌文件夾路徑

    try:
        # 確保日誌文件夾存在
        os.makedirs(log_dir, exist_ok=True)

        # 加載現有數據（如果文件存在且非空）
        if os.path.exists(log_path):
            if os.path.getsize(log_path) > 0:
                try:
                    with open(log_path, "r", encoding='utf-8') as f:
                        data = json.load(f)
                    # 基本驗證，確保讀取的是字典
                    if not isinstance(data, dict):
                         logger.warning(f"日誌文件 {log_path} 根結構唔係字典，將重置。")
                         data = {}
                except json.JSONDecodeError:
                     logger.error(f"無法解析舊嘅成功率日誌 {log_path}，將創建新文件。")
                     # 可以選擇備份損壞文件
                     # try:
                     #     os.rename(log_path, log_path + f".corrupted_{today}")
                     # except OSError as backup_err:
                     #     logger.error(f"備份損壞日誌文件失敗: {backup_err}")
                     data = {} # 如果解析失敗，從空字典開始
            else:
                 data = {} # 文件存在但係空嘅
        else:
             data = {} # 文件唔存在

        # 初始化當天數據結構 (如果需要)
        if today not in data:
            data[today] = {}

        # 初始化當天該 EPIC 的數據結構 (如果需要)
        if epic not in data[today]:
            # 初始化所有預期狀態，方便統計
            data[today][epic] = {
                "SUCCESS": 0, "FAIL": 0, "SKIP_HOLD": 0, "NO_DATA": 0,
                "EXCEPTION_ORDER": 0, "EXCEPTION_ATTR": 0, "EXCEPTION_EPIC": 0,
                "EXCEPTION_RISK": 0, # 增加之前冇嘅
                "UNKNOWN": 0
            }
            # 如果 result 係 HOLD 之外嘅 SKIP (例如 SKIP_BUY), 亦都初始化
            if result.startswith("SKIP_") and result not in data[today][epic]:
                 data[today][epic][result] = 0


        # 累計對應結果嘅次數
        if result in data[today][epic]:
            data[today][epic][result] += 1
        else:
            # 如果遇到一個全新嘅 result 類型，記錄低並初始化為 1
            logger.warning(f"遇到新嘅結果類型 '{result}' for epic '{epic}'，將會記錄。")
            data[today][epic][result] = 1

        # 保存更新後嘅數據
        with open(log_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False) # ensure_ascii=False 避免中文變 unicode
        # logger.info(f"記錄結果 for {epic}: {result}") # 主循環已有日誌，此處可省略

    except Exception as e:
        logger.error(f"寫入策略成功率日誌 {log_path} 時出錯: {e}", exc_info=True)
        print(f"DEBUG: Error writing strategy success log: {e}")


def get_success_rate(epic, days=3):
    """
    計算指定 EPIC 在最近 N 日的成功率 (SUCCESS / (SUCCESS + FAIL))
    """
    data = {}
    if not os.path.exists(log_path):
        logger.warning(f"成功率日誌文件 {log_path} 未找到，無法計算成功率。返回 1.0。")
        return 1.0 # 如果冇歷史記錄，當作 100% 成功率？或者 None / 0.0？

    try:
         if os.path.getsize(log_path) > 0:
             with open(log_path, "r", encoding='utf-8') as f:
                 data = json.load(f)
             if not isinstance(data, dict):
                 logger.error(f"日誌文件 {log_path} 根結構唔係字典，無法計算成功率。返回 0.0。")
                 return 0.0
         else:
             logger.warning(f"成功率日誌文件 {log_path} 為空，無法計算成功率。返回 1.0。")
             return 1.0

    except json.JSONDecodeError:
        logger.error(f"無法解析成功率日誌 {log_path}，無法計算成功率。返回 0.0。")
        return 0.0
    except Exception as e:
        logger.error(f"讀取成功率日誌 {log_path} 時出錯: {e}。返回 0.0。", exc_info=True)
        return 0.0

    total_success = 0
    total_fail = 0
    today = datetime.now().date()

    # 遍歷最近 N 天
    for i in range(days):
        current_date = today - timedelta(days=i)
        date_key = current_date.strftime("%Y-%m-%d")

        if date_key in data and isinstance(data[date_key], dict) and epic in data[date_key]:
             day_data = data[date_key][epic]
             if isinstance(day_data, dict): # 確保 epic 對應嘅係字典
                  total_success += day_data.get("SUCCESS", 0)
                  total_fail += day_data.get("FAIL", 0)

    # 計算成功率
    total_relevant = total_success + total_fail
    if total_relevant == 0:
        logger.info(f"最近 {days} 日內 '{epic}' 冇 SUCCESS 或 FAIL 記錄，無法計算相關成功率。返回 1.0。")
        return 1.0 # 如果冇相關交易，成功率當 100%？
    else:
        rate = round(total_success / total_relevant, 2)
        logger.info(f"計算成功率 for '{epic}' (近 {days} 日): {total_success} / {total_relevant} = {rate:.2%}")
        return rate

# 可以直接運行此文件嚟測試 (可選)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    test_epic = "CS.D.GBPUSD.MINI.IP"
    print(f"Testing log_strategy_result for {test_epic}...")
    log_strategy_result(test_epic, "SUCCESS")
    log_strategy_result(test_epic, "FAIL")
    log_strategy_result(test_epic, "SUCCESS")
    log_strategy_result(test_epic, "SKIP_HOLD")
    log_strategy_result(test_epic, "EXCEPTION_ORDER")
    print(f"Testing get_success_rate for {test_epic}...")
    rate = get_success_rate(test_epic, days=1)
    print(f"Success rate for {test_epic} (last 1 day): {rate:.2%}")
    print("Check logs/strategy_success.json file for results.")
