# /home/hmtf000001/trading_bot/product_filter.py (JSON 讀取版本)

import json
import os
import logging # 使用 logging 記錄錯誤

logger = logging.getLogger(__name__)

# 假設此腳本由位於 trading_bot 根目錄的腳本導入並運行
# 相對路徑 'configs/epic_list.json' 應該可以工作
CONFIG_FILE = 'configs/epic_list.json'

def get_target_products(): # <--- 注意函數名稱係 get_target_products
    """
    從 configs/epic_list.json 讀取目標 EPIC 列表。
    如果文件找不到、格式錯誤或讀取失敗，返回空列表。
    """
    default_products = []
    abs_config_path = os.path.abspath(CONFIG_FILE) # 獲取絕對路徑方便日誌記錄

    try:
        if not os.path.exists(CONFIG_FILE):
            logger.error(f"產品列表文件未找到: {abs_config_path}")
            return default_products

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 假設 JSON 結構係 {"products": ["EPIC1", "EPIC2"]}
            products = data.get("products", default_products)

            # 驗證 products 是否為 list 且 list 內元素是否都為 string
            if isinstance(products, list) and all(isinstance(p, str) for p in products):
                logger.info(f"成功從 {abs_config_path} 加載 {len(products)} 個產品。")
                return products
            else:
                logger.error(f"配置文件 {abs_config_path} 格式錯誤: 'products' 鍵應包含一個字符串列表。 返回空列表。")
                return default_products

    except json.JSONDecodeError:
        logger.error(f"無法解析 JSON 文件: {abs_config_path}", exc_info=True) # 記錄 traceback
        return default_products
    except Exception as e:
        logger.error(f"讀取產品列表 {abs_config_path} 時發生未預期錯誤: {e}", exc_info=True) # 記錄 traceback
        return default_products

# 可以直接運行此文件嚟測試 get_target_products() 功能 (可選)
if __name__ == '__main__':
    # 為直接運行測試配置基本日誌
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    targets = get_target_products()
    print("-" * 20)
    if targets:
        print(f"成功加載目標產品:")
        for target in targets:
            print(f"- {target}")
    else:
        print("未能加載目標產品或列表為空。")
    print("-" * 20)
