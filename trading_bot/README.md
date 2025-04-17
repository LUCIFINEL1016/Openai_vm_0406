# 自動化交易機械人 (v2.4.6-stable 基準)

## 項目概覽

此為一個自動化交易系統，設計用作與 IG Market API (Demo) 互動。

## 文件結構與路徑

* **項目根目錄:** `/home/hmtf000001/trading_bot/`
* **虛擬環境 (venv):** `/home/hmtf000001/trading_bot/venv/`
* **配置文件:** `/home/hmtf000001/trading_bot/configs/` (包含 `.json` 文件，例如 `epic_list.json`, `risk_config.json`)
* **憑證文件:** `/home/hmtf000001/trading_bot/.env` (包含 API Keys, 密碼等 - 使用 `SIM_` 前綴)
* **日誌 (手動/腳本):** `/home/hmtf000001/trading_bot/logs/` (例如 `main_log.txt`, `strategy_success.json`)
* **日誌 (Cron 執行):** `/home/hmtf000001/trading_bot/logs/auto_trading_cron.log`
* **策略:** `/home/hmtf000001/trading_bot/strategies/`
* **工具函數:** `/home/hmtf000001/trading_bot/utils/`
* **依賴列表:** `/home/hmtf000001/trading_bot/requirements.txt`

## 環境設置與執行

1.  **進入項目根目錄:**
    ```bash
    cd /home/hmtf000001/trading_bot/
    ```

2.  **激活虛擬環境:**
    ```bash
    source venv/bin/activate
    ```

3.  **安裝/更新依賴 (如果需要):**
    ```bash
    pip install -r requirements.txt
    ```

4.  **手動運行主腳本:**
    ```bash
    # 確保 venv 已激活
    python auto_trading_unified_sim.py
    ```

## Crontab 配置示例

確保 Crontab (`crontab -e`) 中包含以下或類似的指令 (請用 `crontab -l` 檢查)：

```crontab
# 每日 7:00 AM HKT 運行主腳本
0 7 * * * cd /home/hmtf000001/trading_bot/ && /home/hmtf000001/trading_bot/venv/bin/python auto_trading_unified_sim.py >> /home/hmtf000001/trading_bot/logs/auto_trading_cron.log 2>&1

# 記錄 Cron 觸發時間
0 7 * * * echo "🟢 Cron job triggered for main script at $(date)" >> /home/hmtf000001/trading_bot/logs/cron_trigger.log 2>&1

# 其他 Cron 任務 (例如備份、清理) 如果操作項目文件，亦應使用 /home/hmtf000001/trading_bot/ 下的路徑。
