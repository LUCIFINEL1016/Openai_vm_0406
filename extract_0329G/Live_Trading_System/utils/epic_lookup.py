
def get_epic(symbol: str = "GOLD") -> str:
    # 簡易 EPIC 映射，支援黃金
    epic_map = {
        "GOLD": "CS.D.CFDGOLD.CFDGC.IP"
    }
    return epic_map.get(symbol.upper(), "CS.D.CFDGOLD.CFDGC.IP")
