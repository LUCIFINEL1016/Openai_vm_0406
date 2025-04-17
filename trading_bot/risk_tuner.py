# /home/hmtf000001/trading_bot/risk_tuner.py (函數版本 - 讀取靜態配置)
import json
import os
import logging # 使用 logging

logger = logging.getLogger(__name__)
CONFIG_FILE = 'configs/risk_config.json' # 相對路徑

def get_risk_config(epic: str): # <--- 定義返 get_risk_config 函數
    """
    從 configs/risk_config.json 讀取全局風控參數。
    (注意：目前版本忽略 epic 參數，只讀取全局配置)
    返回包含風險配置的字典。
    """
    # 定義預設值，以防文件讀取失敗或缺少鍵
    default_config = {
        "default_stop": 30,
        "max_risk_per_trade": 0.02,
        "daily_max_risk": 0.1,
        "trailing_stop": True
    }
    abs_config_path = os.path.abspath(CONFIG_FILE)
    print(f"DEBUG: [RiskTuner] Attempting to load risk config from: {abs_config_path}") # DEBUG

    if not os.path.exists(CONFIG_FILE):
        logger.warning(f"⚠️ 風控配置文件未找到: {abs_config_path}. 使用預設值。")
        print(f"DEBUG: [RiskTuner] Config file not found, returning default.") # DEBUG
        return default_config

    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
            # 使用 .get() 提供預設值，增加健壯性
            config = {
                "default_stop": data.get("default_stop", default_config["default_stop"]),
                "max_risk_per_trade": data.get("max_risk_per_trade", default_config["max_risk_per_trade"]),
                "daily_max_risk": data.get("daily_max_risk", default_config["daily_max_risk"]),
                "trailing_stop": data.get("trailing_stop", default_config["trailing_stop"])
            }
            logger.info(f"✅ 成功從 {abs_config_path} 加載風控配置。")
            print(f"DEBUG: [RiskTuner] Config loaded successfully: {config}") # DEBUG
            return config
    except json.JSONDecodeError:
         logger.error(f"❌ 無法解析風控配置文件 JSON: {abs_config_path}. 使用預設值。", exc_info=True)
         print(f"DEBUG: [RiskTuner] JSON decode error, returning default.") # DEBUG
         return default_config
    except Exception as e:
        logger.error(f"❌ 讀取風控配置文件 {abs_config_path} 時出錯: {e}. 使用預設值。", exc_info=True)
        print(f"DEBUG: [RiskTuner] Exception reading config, returning default: {e}") # DEBUG
        return default_config

# 可以直接運行此文件嚟測試 get_risk_config() 功能 (可選)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 假設有個 EPIC 用嚟測試 (雖然目前函數唔用佢)
    test_epic = "CS.D.GBPUSD.MINI.IP"
    risk_settings = get_risk_config(test_epic)
    print("-" * 20)
    if risk_settings:
        print(f"成功加載風險配置:")
        for key, value in risk_settings.items():
             print(f"- {key}: {value}")
    else:
        # 理論上總會返回 default_config
        print("未能加載風險配置 (呢個情況唔應該出現)")
    print("-" * 20)
