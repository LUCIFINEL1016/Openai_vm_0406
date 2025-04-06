
class TradingBot:
    def __init__(self):
        self.cash = 100000
        self.position = 0

    def evaluate_market(self, price):
        print('Evaluating price:', price)
        if price < 1000:
            return "buy"
        elif price > 2000:
            return "sell"
        return "hold"

    def execute_trade(self, signal):
        if signal == "buy":
            self.position += 1
            self.cash -= 1000
        elif signal == "sell" and self.position > 0:
            self.position -= 1
            self.cash += 2000

    def analyze_and_trade(self, symbol, market_data):
        print('market_data keys:', market_data.keys())
        print('symbol used:', symbol)
        signal = self.evaluate_market(market_data.get(symbol.upper(), 1500))
        self.execute_trade(signal)
        return {"signal": signal, "status": self.status()}

    def status(self):
        return {"cash": self.cash, "position": self.position}

TradingStrategy = TradingBot
