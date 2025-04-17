# ig_api_client.py (經 AI 修改 V2 - 添加 authenticated 屬性)
import requests
import os
from dotenv import load_dotenv
import logging # 建議使用 logging 而唔係 print

load_dotenv(dotenv_path="/home/hmtf000001/.env", verbose=True)

# 獲取 logger 實例
logger = logging.getLogger(__name__)
# 設置基本配置 (如果冇喺主腳本設置過)
if not logger.hasHandlers():
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class IGClient:
    def __init__(self):
        # --- DEBUG ---
        print("DEBUG: IGClient __init__ started")
        self.username = os.getenv("SIM_IG_USERNAME")
        self.password = os.getenv("SIM_IG_PASSWORD")
        self.api_key = os.getenv("SIM_IG_API_KEY")
        self.account_id = os.getenv("SIM_IG_ACC_ID") # 假設 Account ID 都需要用 SIM_

        self.base_url = "https://demo-api.ig.com/gateway/deal" # Demo API
        self.session = requests.Session()
        self.headers = {
            "X-IG-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json; charset=UTF-8",
            "IG-ACCOUNT-ID": self.account_id # 有啲 API 可能需要喺 header 加 account id
        }
        self.authenticated = False # <--- 新增：初始化 authenticated 狀態
        print("DEBUG: IGClient basic attributes set, attempting login...")
        self._login()
        print("DEBUG: IGClient __init__ finished")


    def _login(self):
        # --- DEBUG ---
        print("DEBUG: IGClient _login() started")
        if not self.username or not self.password or not self.api_key:
             logger.error("❌ IG 登錄失敗：缺少用戶名、密碼或 API Key 環境變數。")
             print("DEBUG: Missing credentials in environment variables.")
             self.authenticated = False # 確保狀態係 False
             return

        payload = {
            "identifier": self.username,
            "password": self.password
        }

        # --- DEBUG ---
        print(f"DEBUG: Preparing to POST to {self.base_url}/session")
        try:
            response = self.session.post(
                f"{self.base_url}/session",
                json=payload,
                headers={"X-IG-API-KEY": self.api_key, "Version": "2"} # 登錄 API 可能需要 Version header
            )
            # --- DEBUG ---
            print(f"DEBUG: Login response status code: {response.status_code}")
            # print(f"DEBUG: Login response headers: {response.headers}") # 可以取消註釋睇詳細 header

            if response.status_code == 200:
                # 從 Header 獲取安全令牌
                security_token = response.headers.get("X-SECURITY-TOKEN")
                cst_token = response.headers.get("CST")

                if security_token and cst_token:
                    self.headers["X-SECURITY-TOKEN"] = security_token
                    self.headers["CST"] = cst_token
                    self.authenticated = True # <--- 新增：設置 authenticated 為 True
                    logger.info("✅ IG 登入成功")
                    print("DEBUG: IG Login successful, tokens received, authenticated=True")
                else:
                    logger.error("❌ IG 登錄成功但未返回必要嘅 Tokens (X-SECURITY-TOKEN/CST)")
                    print("DEBUG: Login status 200 but missing tokens in headers.")
                    self.authenticated = False # 缺少 token 亦視為未成功驗證

            else:
                logger.error(f"❌ IG 登錄失敗，狀態碼：{response.status_code}, 響應：{response.text}")
                print(f"DEBUG: Login failed with status code {response.status_code}")
                self.authenticated = False # 登錄失敗

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ IG 登錄請求異常：{e}")
            print(f"DEBUG: Exception during login request: {e}")
            self.authenticated = False # 請求異常亦視為未成功
        # --- DEBUG ---
        print("DEBUG: IGClient _login() finished")


    def create_position(self, epic, direction, size=1, stop_distance=30):
        """
        實際 IG 下單動作（MARKET）
        """
        # --- DEBUG ---
        print(f"DEBUG: create_position called with: epic={epic}, direction={direction}, size={size}, stop_distance={stop_distance}")

        if not self.authenticated:
            logger.warning("⚠️ 嘗試下單但未登入")
            print("DEBUG: create_position failed: not authenticated")
            return {"success": False, "error": "未登入"}

        # 準備下單 payload (留意 IG API 可能需要嘅字段)
        payload = {
            "epic": epic,
            "direction": direction, # "BUY" or "SELL"
            "size": str(size), # IG API 通常要求 size 係 string
            "orderType": "MARKET",
            "expiry": "-", # MARKET 單通常用 "-"
            "guaranteedStop": False, # 或者根據需要設定 True
            "stopDistance": str(stop_distance), # 止損距離
            # "limitDistance": str(limit_distance), # 如果需要止盈，create_position 冇呢個參數
            "forceOpen": True, # 強制開新倉
            "currencyCode": "USD", # 根據商品貨幣設定，或者留空由 API 判斷?
            # "dealReference": os.urandom(10).hex().upper() # dealReference 通常由 API 返回，唔係自己生成
        }
        # --- DEBUG ---
        print(f"DEBUG: Preparing to POST to {self.base_url}/positions/otc with payload: {payload}")

        try:
            response = self.session.post(
                f"{self.base_url}/positions/otc",
                json=payload,
                headers=self.headers # 使用包含 token 嘅 headers
            )
            # --- DEBUG ---
            print(f"DEBUG: Create position response status code: {response.status_code}")
            print(f"DEBUG: Create position response content: {response.text}") # 睇下 API 返回乜嘢

            response_data = response.json()

            if response.status_code == 200: # 有啲 API 成功係 200
                deal_reference = response_data.get("dealReference")
                if deal_reference:
                     logger.info(f"✅ IG 下單請求成功，DealRef: {deal_reference}")
                     print(f"DEBUG: create_position successful, dealRef: {deal_reference}")
                     return {
                         "success": True,
                         "deal_reference": deal_reference,
                         "epic": epic,
                         "direction": direction
                     }
                else:
                     logger.warning(f"⚠️ IG 下單請求狀態碼 200 但未返回 dealReference: {response_data}")
                     print("DEBUG: create_position status 200 but no dealReference.")
                     return {"success": False, "error": "狀態碼 200 但未返回 Deal Reference", "response": response_data}
            else:
                error_message = response_data.get("errorCode") or response_data.get("message", response.text)
                logger.error(f"❌ IG 下單請求失敗，狀態碼：{response.status_code}, 錯誤：{error_message}")
                print(f"DEBUG: create_position failed with status {response.status_code}, error: {error_message}")
                return {
                    "success": False,
                    "error": error_message,
                    "status_code": response.status_code,
                    "response": response_data
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ IG 下單請求異常：{e}")
            print(f"DEBUG: Exception during create_position request: {e}")
            return {"success": False, "error": f"請求異常: {str(e)}"}

    # --- 可以在這裡添加 get_price_history 等其他需要嘅方法 ---
    # def get_price_history(self, epic, resolution='D', num_points=100):
    #     """獲取價格歷史數據 (示例，需要根據 IG API 文檔實現)"""
    #     if not self.authenticated:
    #         logger.warning("⚠️ 嘗試獲取價格但未登入")
    #         return None
    #     # ... 實現調用 IG API /prices/{epic} 端點嘅邏輯 ...
    #     # endpoint = f"{self.base_url}/prices/{epic}?resolution={resolution}&max={num_points}"
    #     # response = self.session.get(endpoint, headers=self.headers)
    #     # ... 處理響應，轉換成 pandas DataFrame/Series ...
    #     logger.warning(f"ℹ️ get_price_history 方法尚未完全實現") # 提示
    #     return None # 暫時返回 None
