import requests
import time

class AutoReAuthHandler:
    def __init__(self, api_url, username, password, api_key):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.api_key = api_key
        self.cst = None
        self.security_token = None
        self.authenticate()

    def authenticate(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-IG-API-KEY': self.api_key
        }
        data = {
            'identifier': self.username,
            'password': self.password
        }
        response = requests.post(f'{self.api_url}/session', headers=headers, json=data)
        if response.status_code == 200:
            self.cst = response.headers.get('CST')
            self.security_token = response.headers.get('X-SECURITY-TOKEN')
            print("Token refreshed.")
        else:
            print(f"Auth failed: {response.status_code} - {response.text}")

    def get_auth_headers(self):
        if not self.cst or not self.security_token:
            self.authenticate()
        return {
            'X-IG-API-KEY': self.api_key,
            'CST': self.cst,
            'X-SECURITY-TOKEN': self.security_token
        }
