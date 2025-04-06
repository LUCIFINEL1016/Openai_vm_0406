import json
import requests
from utils.ig_auth import IGSession
from utils.ig_order_helper import prepare_order_payload

class AutoOrderIG:
    def __init__(self, config_path='config/live_ig_config.json'):
        self.config_path = config_path
        self.session = None
        self.headers = {}

    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config

    def login(self):
        config = self.load_config()
        self.session = IGSession(
            api_key=config['api_key'],
            identifier=config['identifier'],
            password=config['password']
        )
        self.session.authenticate()
        self.headers = self.session.get_headers()

    def place_order(self, epic, size, direction, level, stop_distance, limit_distance):
        payload = prepare_order_payload(
            epic=epic,
            size=size,
            direction=direction,
            level=level,
            stop_distance=stop_distance,
            limit_distance=limit_distance,
            force_open=True,
            guaranteed_stop=False,
            order_type='LIMIT',
            time_in_force='GTC'
        )
        response = requests.post(
            url=self.session.base_url + "/gateway/deal/positions",
            data=json.dumps(payload),
            headers=self.headers
        )
        if response.status_code == 200:
            print("✅ 自動訂單已送出：", response.json())
            return True
        else:
            print("❌ 下單失敗：", response.text)
            return False

if __name__ == '__main__':
    trader = AutoOrderIG()
    trader.login()

    # 自動從策略模組取得操作建議（範例模擬邏輯）
    from strategy.strategy_engine import get_trade_signal

    trade_signal = get_trade_signal('GOLD')
    if trade_signal:
        trader.place_order(
            epic=trade_signal['epic'],
            size=trade_signal['size'],
            direction=trade_signal['direction'],
            level=trade_signal['entry'],
            stop_distance=trade_signal['stop'],
            limit_distance=trade_signal['limit']
        )
    else:
        print("今日無黃金交易建議，無自動掛單。")
