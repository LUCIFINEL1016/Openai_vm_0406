# /home/hmtf000001/trading_bot/ig_api_client.py
# 版本：經 AI 修改 V5 - 使用 V3 Prices Endpoint + Query Params

import requests
import os
import logging
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta, timezone # 確保導入

# 加載 .env (應能自動找到 trading_bot/.env)
print("DEBUG: [ig_api_client.py] Attempting to load .env file...")
loaded = load_dotenv(verbose=True)
print(f"DEBUG: [ig_api_client.py] load_dotenv result: {loaded}")

# 獲取 logger 實例
logger = logging.getLogger(__name__)
if not logging.getLogger().hasHandlers():
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
     logger.info("Basic logging configured by ig_api_client.")


class IGClient:
    def __init__(self):
        # --- DEBUG ---
        print("DEBUG: IGClient __init__ started")
        self.username = os.getenv("SIM_IG_USERNAME")
        self.password = os.getenv("SIM_IG_PASSWORD")
        self.api_key = os.getenv("SIM_IG_API_KEY")
        self.account_id = os.getenv("SIM_IG_ACC_ID")

        # --- DEBUG 打印讀取到的憑證 ---
        print(f"DEBUG: Read SIM_IG_USERNAME: [{'******' if self.username else 'Not Found'}]")
        print(f"DEBUG: Read SIM_IG_PASSWORD: [{'******' if self.password else 'Not Found'}]")
        print(f"DEBUG: Read SIM_IG_API_KEY: [{'******' if self.api_key else 'Not Found'}]")
        print(f"DEBUG: Read SIM_IG_ACC_ID: [{'******' if self.account_id else 'Not Found'}]")
        # --- /DEBUG ---

        self.base_url = "https://demo-api.ig.com/gateway/deal"
        self.session = requests.Session()
        self.headers = {
            "X-IG-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json; charset=UTF-8",
            "IG-ACCOUNT-ID": self.account_id
        }
        self.authenticated = False # 初始化 authenticated 狀態
        print("DEBUG: IGClient basic attributes set, attempting login...")
        self._login()
        print("DEBUG: IGClient __init__ finished")


    def _login(self):
        print("DEBUG: IGClient _login() started")
        if not self.username or not self.password or not self.api_key:
             logger.error("❌ IG 登錄失敗：缺少用戶名、密碼或 API Key 環境變數。")
             print("DEBUG: Missing credentials in environment variables.")
             self.authenticated = False
             return

        payload = { "identifier": self.username, "password": self.password }
        print(f"DEBUG: Preparing to POST to {self.base_url}/session")
        try:
            response = self.session.post(
                f"{self.base_url}/session",
                json=payload,
                headers={"X-IG-API-KEY": self.api_key, "Version": "2"} # 登錄繼續用 V2
            )
            print(f"DEBUG: Login response status code: {response.status_code}")

            if response.status_code == 200:
                security_token = response.headers.get("X-SECURITY-TOKEN")
                cst_token = response.headers.get("CST")
                if security_token and cst_token:
                    self.headers["X-SECURITY-TOKEN"] = security_token
                    self.headers["CST"] = cst_token
                    self.authenticated = True # 設置為 True
                    logger.info("✅ IG 登入成功")
                    print("DEBUG: IG Login successful, tokens received, authenticated=True")
                else:
                    logger.error("❌ IG 登錄成功但未返回必要嘅 Tokens")
                    print("DEBUG: Login status 200 but missing tokens.")
                    self.authenticated = False
            else:
                logger.error(f"❌ IG 登錄失敗，狀態碼：{response.status_code}, 響應：{response.text}")
                print(f"DEBUG: Login failed with status code {response.status_code}")
                self.authenticated = False

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ IG 登錄請求異常：{e}")
            print(f"DEBUG: Exception during login request: {e}")
            self.authenticated = False
        print("DEBUG: IGClient _login() finished")


    def create_position(self, epic, direction, size=1, stop_distance=30):
        """ 實際 IG 下單動作（MARKET） """
        print(f"DEBUG: create_position called with: epic={epic}, direction={direction}, size={size}, stop_distance={stop_distance}")
        if not self.authenticated:
            logger.warning("⚠️ 嘗試下單但未登入")
            print("DEBUG: create_position failed: not authenticated")
            return {"success": False, "error": "未登入"}

        payload = {
            "epic": epic, "direction": direction, "size": str(size),
            "orderType": "MARKET", "expiry": "-", "guaranteedStop": False,
            "stopDistance": str(stop_distance), "forceOpen": True, "currencyCode": "USD",
        }
        print(f"DEBUG: Preparing to POST to {self.base_url}/positions/otc with payload: {payload}")
        try:
            response = self.session.post(f"{self.base_url}/positions/otc", json=payload, headers=self.headers) # 落單唔需要 Version header? Check docs if needed
            print(f"DEBUG: Create position response status code: {response.status_code}")
            print(f"DEBUG: Create position response content: {response.text}")
            response_data = response.json()

            if response.status_code == 200:
                deal_reference = response_data.get("dealReference")
                if deal_reference:
                     logger.info(f"✅ IG 下單請求成功，DealRef: {deal_reference}")
                     print(f"DEBUG: create_position successful, dealRef: {deal_reference}")
                     return {"success": True, "deal_reference": deal_reference, "epic": epic, "direction": direction}
                else:
                     logger.warning(f"⚠️ IG 下單請求狀態碼 200 但未返回 dealReference: {response_data}")
                     print("DEBUG: create_position status 200 but no dealReference.")
                     return {"success": False, "error": "狀態碼 200 但未返回 Deal Reference", "response": response_data}
            else:
                error_message = response_data.get("errorCode") or response_data.get("message", response.text)
                logger.error(f"❌ IG 下單請求失敗，狀態碼：{response.status_code}, 錯誤：{error_message}")
                print(f"DEBUG: create_position failed with status {response.status_code}, error: {error_message}")
                return {"success": False, "error": error_message, "status_code": response.status_code, "response": response_data}
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ IG 下單請求異常：{e}")
            print(f"DEBUG: Exception during create_position request: {e}")
            return {"success": False, "error": f"請求異常: {str(e)}"}
        except Exception as e:
             logger.error(f"❌ 處理下單響應時出錯: {e}", exc_info=True)
             print(f"DEBUG: Error processing create_position response: {e}")
             return {"success": False, "error": f"處理響應錯誤: {str(e)}"}


    # --- 使用 V3 端點 + Query Params 嘅 get_price_history ---
    def get_price_history(self, epic: str, resolution: str = 'DAY', num_points: int = 20):
        """
        獲取指定 EPIC 的歷史價格數據 (使用 V3 端點 + Query Params: /prices/{epic}?resolution=...&max=...)。
        注意：Response 結構需要根據實際返回核對！
        """
        global logger
        logger.info(f"嘗試為 {epic} 獲取 {num_points} 點 {resolution} 週期價格數據 (使用 V3 API Query Params)...")
        print(f"DEBUG: get_price_history called for {epic}, resolution={resolution}, num_points={num_points}")

        if not self.authenticated:
            logger.warning(f"⚠️ 嘗試獲取 {epic} 價格但未登入")
            print("DEBUG: get_price_history failed: not authenticated")
            return None

        # --- 使用 V3 Endpoint Path ---
        endpoint = f"{self.base_url}/prices/{epic}" # <-- V3 URL Structure

        # --- 使用 Query Parameters ---
        params = {
            'resolution': resolution,  # 使用 'DAY'
            'max': str(num_points)     # 使用 max 參數
        }
        print(f"DEBUG: Using query params: {params}")

        # --- 使用 V3 Headers ---
        request_headers = self.headers.copy()
        request_headers['Version'] = '3' # <--- 指定使用 API 版本 3

        print(f"DEBUG: Calling V3 price history endpoint: {endpoint}")
        print(f"DEBUG: Using headers: {request_headers}")

        try:
            response = self.session.get(endpoint, headers=request_headers, params=params, timeout=15) # <-- 使用 params
            print(f"DEBUG: Price history response status code: {response.status_code}")
            print(f"DEBUG: Price history response text (first 500 chars): {response.text[:500]}")

            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG: Price history JSON response data (partial): {str(data)[:500]}") # <-- 留意呢度輸出

                # --- 解析 JSON (根據 V3 文檔示例調整) ---
                prices_list = None
                allowance = data.get('allowance')
                metadata = data.get('metadata')
                if allowance: print(f"DEBUG: API Allowance: {allowance.get('remainingAllowance')} / {allowance.get('totalAllowance')}")
                if metadata: print(f"DEBUG: Paging info: {metadata.get('paging')}")

                if 'prices' in data and isinstance(data['prices'], list):
                     prices_list = data['prices']

                if prices_list is None:
                     logger.warning(f"⚠️ API 為 {epic} 返回嘅數據格式不符或缺少 'prices' 列表鍵。 Data: {str(data)[:200]}")
                     print(f"DEBUG: Unexpected data format or missing 'prices' list key for {epic}.")
                     return None
                if not prices_list:
                     logger.warning(f"⚠️ API 為 {epic} 返回了空的價格列表。")
                     print(f"DEBUG: Empty price list received for {epic}.")
                     return None

                # --- 解析價格點 (V3 結構睇落同之前猜測吻合) ---
                timestamps = []
                close_bids = []
                for price_point in prices_list:
                    if not isinstance(price_point, dict): continue
                    try:
                        ts_str = price_point.get('snapshotTimeUTC') # V3 用 UTC
                        timestamp = pd.to_datetime(ts_str, utc=True) if ts_str else None # 指定 UTC

                        bid_price = None
                        if 'closePrice' in price_point and isinstance(price_point['closePrice'], dict):
                             bid_price = price_point['closePrice'].get('bid')

                        if timestamp is not None and bid_price is not None:
                            timestamps.append(timestamp)
                            close_bids.append(float(bid_price))
                        else:
                            logger.warning(f"  ⚠️ 跳過無效價格點 (缺少時間或 closePrice.bid): {price_point}")

                    except Exception as e:
                         logger.warning(f"  ⚠️ 解析價格點 {price_point} 時出錯: {e}", exc_info=False)
                         continue

                if not close_bids:
                    logger.error(f"❌ 無法從 API 響應中為 {epic} 解析出有效的價格數據。")
                    print(f"DEBUG: Failed to parse valid prices for {epic}.")
                    return None

                # 創建 Pandas Series，確保 index 是 DatetimeIndex[UTC]
                price_series = pd.Series(close_bids, index=pd.DatetimeIndex(timestamps, name="Timestamp"))
                price_series = price_series.sort_index()
                logger.info(f"✅ 成功為 {epic} 獲取並解析了 {len(price_series)} 個 V3 價格點。")
                print(f"DEBUG: Parsed price series for {epic} with {len(price_series)} points.")
                return price_series
                # --- /解析 JSON ---

            else: # status_code not 200
                error_message = "未知錯誤"
                try:
                    error_data = response.json()
                    error_message = error_data.get("errorCode") or error_data.get("message", response.text)
                except ValueError:
                    error_message = response.text[:200]
                logger.error(f"❌ 獲取 {epic} 價格失敗，狀態碼：{response.status_code}, 錯誤：{error_message}")
                print(f"DEBUG: Get price history failed with status {response.status_code}, error: {error_message}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 獲取 {epic} 價格請求異常：{e}")
            print(f"DEBUG: Exception during get_price_history request: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ 處理 {epic} 價格數據時發生未預期錯誤: {e}", exc_info=True)
            print(f"DEBUG: Unexpected error during get_price_history processing: {e}")
            return None

    # --- 其他需要嘅 IGClient 方法可以繼續加喺下面 ---

# (IGClient class 嘅結束位置)
