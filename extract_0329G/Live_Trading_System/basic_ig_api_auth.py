
import requests

def ig_login(api_key, identifier, password):
    url = "https://api.ig.com/gateway/deal/session"
    headers = {
        "X-IG-API-KEY": api_key,
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json"
    }
    payload = {
        "identifier": identifier,
        "password": password
    }
    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        cst = resp.headers.get("CST")
        sst = resp.headers.get("X-SECURITY-TOKEN")
        print("[登入成功] CST:", cst[:6], "... SST:", sst[:6], "...")
        return {"CST": cst, "X-SECURITY-TOKEN": sst}
    except Exception as e:
        print("[登入失敗]", e)
        return None
