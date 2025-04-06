# api_key_manager.py - Integrated on 2025-03-27
# Live_Trading_System/api_key_manager.py

def get_api_key(source):
    demo_keys = {
        "ALPHA": "demo_alpha_key",
        "FRED": "demo_fred_key"
    }
    return demo_keys.get(source, "unknown_key")

