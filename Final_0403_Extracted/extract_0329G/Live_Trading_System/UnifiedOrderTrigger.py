
from Live_Trading_System.AutoOrder_Fallback_Gold0326D import fallback_gold_order
from Live_Trading_System.AutoOrder_Fallback_USOIL0329 import fallback_oil_order
from Live_Trading_System.AutoOrder_Fallback_EURUSD0329 import fallback_eurusd_order

def trigger_order(symbol: str, price: float, quantity: float):
    symbol = symbol.upper()
    if symbol == "GOLD":
        return fallback_gold_order(price, quantity)
    elif symbol == "USOIL":
        return fallback_oil_order(price, quantity)
    elif symbol == "EURUSD":
        return fallback_eurusd_order(price, quantity)
    else:
        raise ValueError(f"❌ 不支援的標的: {symbol}")
