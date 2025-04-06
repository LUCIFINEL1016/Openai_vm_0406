import requests
from dotenv import load_dotenv
import os

# 加載環境變數
load_dotenv()

# 從 .env 文件中讀取 API 密鑰
LIVE_IG_API_KEY = os.getenv("LIVE_IG_API_KEY")

# 設置 API 請求的頭部
headers = {
    "X-IG-API-KEY": LIVE_IG_API_KEY,
    "Content-Type": "application/json"
}

# 發送請求以檢查是否能夠連接
url = "https://api.ig.com/gateway/deal/session"
response = requests.get(url, headers=headers)

# 檢查連接結果
if response.status_code == 200:
    print("IG API connection successful!")
else:
    print(f"Failed to connect to IG API: {response.status_code}")
