
import os
from dotenv import load_dotenv

load_dotenv()

def get_ig_headers():
    IG_API_KEY = os.getenv("IG_API_KEY")
    IG_USERNAME = os.getenv("IG_USERNAME")
    IG_PASSWORD = os.getenv("IG_PASSWORD")
    IG_ACC_ID = os.getenv("IG_ACC_ID")

    # 模擬取得 CST / X-SECURITY-TOKEN（實務請替換為真實 IG 認證）
    CST = "mock-cst-token"
    SECURITY_TOKEN = "mock-sec-token"
    IG_URL = "https://api.ig.com"

    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "CST": CST,
        "X-SECURITY-TOKEN": SECURITY_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    return headers, IG_URL
