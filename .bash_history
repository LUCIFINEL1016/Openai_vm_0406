python3 --version
pip3 install requests
pip3 install apscheduler
pip3 install json
pip show requests
pip show apscheduler
python3 -c "import json; print(json.__version__)"
import requests
import apscheduler
print("Libraries loaded successfully!")
python3
import requests
import json
# 請填入您的資料
API_KEY = "33012a1647711990919caf823cfaa88765bec64e"  # 請使用您的 API Key
USERNAME = "LUCIFINIL"  # 請填寫您的 IG 帳戶名稱
PASSWORD = "S22334455s"  # 請填寫您的 IG 密碼
# 登錄 IG
def login_ig(api_key, username, password):
# 使用您的 API Key 和帳號登錄
cst, x_token = login_ig(API_KEY, USERNAME, PASSWORD)
python3
我的意思係,訂單已成功在jupyter發送到yg market中,正式倉和模擬倉皆成功在ui界面顯示。現在想要確保該代碼在VM上每日不中斷地實行下單，並符合以下要求
所有設置要求(04/04/2025)
-每日早上6點(香港時間HKT)前自動下訂單(正式倉)
-每日自行運作按市場實際情況(ig market)下訂單
-掛單,市價單皆可
-確保每筆建議有參考所有已整合的模組
-每日最低盈利目標$1000HKD,不設上限
-由低風險,小額倉做起
-產品不限
-見好就收,保本止損優先
-做好風險管理,倉位量力而為
-每日交易量自行決定,可以直到美盤收市為止,翌日6點前可以自行下訂單
-安全至上,避免不必要的虧損
-將系統所有的策略模組(技術/市場新聞模組)都用上
-每日自行檢查有否api key將到期
-時間,ig market市價,指標必須同步
-留意周未周日的假期,紅日,自行調整休市日安排
將以上的條件按目前系統的代碼設置好,整合至主模式
問題係,點樣令個代碼可以在VM上面唔斷線,唔會中斷自動交易系統運作?
nano /home/your-username/auto_trade.py
pwd
nano /home/hmtf000001/auto_trade.py
ls /home/hmtf000001/
ls /home/hmtf000001/
cd /home/hmtf000001/
python3 auto_trade.py
cd /home/hmtf000001/
nano auto_trade.py
python3 auto_trade.py
crontab -e
timedatectl
sudo timedatectl set-timezone Asia/Hong_Kong
timedatectl
crontab -e
crontab -l
/usr/bin/python3 /home/hmtf000001/extract_0329G/Live_Trading_System/trading_live.py
cat /home/hmtf000001/auto_trade.log
mkdir -p /home/hmtf000001/logs
python3 /home/hmtf000001/extract_0329G/Live_Trading_System/trading_live.py
tail -n 50 /home/hmtf000001/logs/trading_live.log
python3
cd /home/hmtf000001/
nano auto_trade.py
cd /home/hmtf000001/
python3 auto_trade.py | tee -a auto_trade.log
cd /home/hmtf000001/
nano auto_trade.py
nano /home/hmtf000001/auto_trade.py
python3 /home/hmtf000001/auto_trade.py | tee -a auto_trade.log
/home/hmtf000001/auto_trade.py
chmod +x /home/hmtf000001/auto_trade.py
/home/hmtf000001/auto_trade.py
python3 /home/hmtf000001/auto_trade.py
nano /home/hmtf000001/auto_trade.py
nano /home/hmtf000001/auto_trade.py
chmod +x /home/hmtf000001/auto_trade.py
python3 /home/hmtf000001/auto_trade.py
crontab -e
crontab -l
cd /home/hmtf000001/
nano auto_trade.py
cd /home/hmtf000001/
nano auto_trade.py
gcloud compute ssh auto-trading-vm --zone=asia-east1-c
nano ~/daily_ai_trade.py
python3 ~/daily_ai_trade.py
crontab -e
nano ~/daily_ai_trade.py
nano test_order.py
python3 test_order.py
scp -i ~/.ssh/auto_ai_key ~/Downloads/daily_ai_trade_final.py hmtf000001@34.81.174.154:~/
scp -i ~/.ssh/auto_ai_key ~/Downloads/daily_ai_trade_final.py hmtf000001@<你的_VM_IP>:~/
scp -i ~/.ssh/auto_ai_key ~/Downloads/daily_ai_trade_final.py hmtf000001@34.81.174.154:~/
test_order.py
nano test_order.py
python3 test_order.py
nano test_order.py
python3 test_order.py
nano test_order.py
python3 test_order.py
nano test_order.py
python3 test_order.py
cd /path/to/your/folder
unzip risk_control_module_FULL.zip
python3 test_order_risk_control.py
python3 test_order_risk_control.py
unzip test_order_risk_control_v2.zip
python3 test_order_risk_control_v2.py
python3 test_order_risk_control_v3.py
python3 test_order_fx_v1.py
python3 test_order_mini_safe_v1.py
mv /mnt/data/test_order_mini_safe_v1.py .
python3 test_order_mini_safe_v1.py
mv /mnt/data/test_order_mini_safe_v1.py .
python3 test_order_mini_safe_v1.py
nano test_order.py
python3 test_order.py
ps aux | grep python
ps aux | grep auto_trade.py
python3 /path/to/auto_trade.py
ls
sudo find / -name "auto_trade.py"
cd /home/hmtf000001/
python3 auto_trade.py
nano /home/hmtf00001/start_auto_trade.sh
nano /home/hmtf00001/start_auto_trade.sh
ls /home/hmtf00001/
mkdir -p /home/hmtf00001/
ls -l /home/hmtf00001/
whoami
sudo mkdir -p /home/hmtf00001/
sudo ls -l /home/
ls -ld /home/hmtf00001
sudo chown -R hmtf00001:hmtf00001 /home/hmtf00001
cat /etc/passwd | grep hmtf00001
sudo chown -R hmtf0001:hmtf0001 /home/hmtf0001
whoami
cat /etc/passwd
sudo chown -R hmtf000001:hmtf000001 /
lsblk
sudo fdisk /dev/sdb
sudo apt update
sudo apt install fdisk
sudo fdisk /dev/sdb
sudo mount /dev/sdb1 /mnt
ls /mnt
ls -l /mnt
sudo fdisk -l
sudo mount /dev/sdb1 /mnt
ls /mnt
ls -l /mnt
ls -l /mnt/home
cp -r /mnt/home/username /home/
cp -r /mnt/home/hmtf000001 /home/
sudo cp -r /mnt/home/hmtf000001 /home/
ls -l /mnt/home/
ls -l /mnt/home/hmtf000001
sudo cp -r /mnt/home/hmtf000001/* /home/hmtf00001/
sudo cp -r /mnt/home/hmtf00001/* /home/hmtf00001/
sudo mkdir -p /home/hmtf000001
sudo cp -r /mnt/home/hmtf000001/* /home/hmtf00001/
ls -l /mnt/home/hmtf000001
cd /home/hmtf000001
sudo mkdir -p /home/hmtf000001/code
sudo mkdir -p /home/hmtf000001/backups
sudo mkdir -p /home/hmtf000001/data
sudo mkdir -p /home/hmtf000001/config
ls -l /home/hmtf000001/
sudo mkdir -p /home/hmtf000001/logs
sudo mkdir -p /home/hmtf000001/temp
ls -l /home/hmtf000001/
sudo mv /home/hmtf000001/auto_backup.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/auto_trade.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/nano.save /home/hmtf000001/temp/
sudo mv /home/hmtf000001/test_order_package.zip /home/hmtf000001/temp/
sudo mv /home/hmtf000001/backup.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/config_file.conf /home/hmtf000001/config/
ls /home/hmtf000001/
ls /home/hmtf000001/backup.zip
sudo mkdir -p /home/hmtf000001/code
sudo mkdir -p /home/hmtf000001/backups
sudo mkdir -p /home/hmtf000001/data
sudo mkdir -p /home/hmtf000001/config
sudo mkdir -p /home/hmtf000001/logs
sudo mkdir -p /home/hmtf000001/temp
ls -l /home/hmtf000001/
sudo mv /home/hmtf000001/auto_trade.py /home/hmtf000001/code/
sudo mv /home/hmtf000001/auto_trade.py.save /home/hmtf000001/code/
sudo mv /home/hmtf000001/auto_start.sh /home/hmtf000001/code/
sudo mv /home/hmtf000001/auto_backup.sh /home/hmtf000001/code/
sudo mv /home/hmtf000001/automated_trading_v1.py /home/hmtf000001/code/
sudo mv /home/hmtf000001/daily_ai_trade.py /home/hmtf000001/code/
sudo mv /home/hmtf000001/daily_ai_trade_final.py /home/hmtf000001/code/
sudo mv /home/hmtf000001/backup_log /home/hmtf000001/code/
ls /home/hmtf000001/auto_trade.py
ls /home/hmtf000001/
sudo find / -name "auto_trade.py"
sudo mv /mnt/home/hmtf000001/auto_trade.py /home/hmtf000001/code/
ls /home/hmtf000001/code/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_AUTO_BACKUP_20250401.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_AUTO_BACKUP_20250402.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_AUTO_BACKUP_20250403.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_AUTO_BACKUP_20250404.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_AUTO_BACKUP_20250405.zip /home/hmtf000001/backups/
sudo mv /home/hmtf000001/deploy.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/extract_0329M.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/extract_0329.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/extract_fixed.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/final_system.zip /home/hmtf000001/data/
sudo find /home/hmtf000001/ -name "extract_0329M.zip"
sudo find /home/hmtf000001/ -name "extract_0329.zip"
sudo find /home/hmtf000001/ -name "*.zip"
sudo mv /home/hmtf000001/deploy.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/extract_fixed.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/final_system.zip /home/hmtf000001/data/
sudo find /home/hmtf000001/ -name "deploy.zip"
sudo find /home/hmtf000001/ -name "extract_fixed.zip"
sudo find /home/hmtf000001/ -name "final_system.zip"
ls /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/deploy.zip -d /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/extract_fixed.zip -d /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/final_system.zip -d /home/hmtf000001/data/
sudo apt update
sudo apt install unzip
sudo unzip /home/hmtf000001/data/deploy.zip -d /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/extract_fixed.zip -d /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/final_system.zip -d /home/hmtf000001/data/
sudo mv /home/hmtf000001/nano.save /home/hmtf000001/temp/
sudo mv /home/hmtf000001/test_order_package.zip /home/hmtf000001/temp/
ls /home/hmtf000001/
sudo find /home/hmtf000001/ -name "*.zip"
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331A.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331C_FULL_REBUILT_(6).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/test_order_risk_control_v2.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP_FIXED_(1).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/auto_ai_ssh_key_bundle.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331C_FULL_REBUILT_(2).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP_FIXED.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_FULL_0403_VERIFIED.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Auto_Trade_Full_Deploy_0330.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0330A_VERIFIED_OK.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/risk_control_module_FULL.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331A.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331C_FULL_REBUILT_\(6\).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/test_order_risk_control_v2.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP_FIXED_\(1\).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/auto_ai_ssh_key_bundle.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331C_FULL_REBUILT_\(2\).zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Extract_0329M_GCP_FIXED.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_FULL_0403_VERIFIED.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Auto_Trade_Full_Deploy_0330.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/Final_Integrated_Trading_System_Optimized_0330A_VERIFIED_OK.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/risk_control_module_FULL.zip /home/hmtf000001/data/
ls /home/hmtf000001/
sudo find / -name "Final_Integrated_Trading_System_Optimized_0331A.zip"
sudo find / -name "test_order_risk_control_v2.zip"
sudo mv /mnt/home/hmtf000001/Final_Integrated_Trading_System_Optimized_0331A.zip /home/hmtf000001/data/
sudo mv /home/hmtf000001/data/home/hmtf000001/extract_0329M/Final_Integrated_Trading_System_Optimized_0331A.zip /home/hmtf000001/data/
sudo mv /mnt/home/hmtf000001/test_order_risk_control_v2.zip /home/hmtf000001/data/
ls /home/hmtf000001/data/
sudo unzip /home/hmtf000001/data/Final_Integrated_Trading_System_Optimized_0331A.zip -d /home/hmtf000001/data/
y
sudo unzip /home/hmtf000001/data/Final_Integrated_Trading_System_Optimized_0331A.zip -d /home/hmtf000001/data/
sudo mv /home/hmtf000001/auto_backup.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/auto_trade.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/jupyter.log /home/hmtf000001/logs/
sudo find /home/hmtf000001/ -name "auto_backup.log"
sudo find /home/hmtf000001/ -name "auto_trade.log"
sudo mv /home/hmtf000001/logs/auto_backup.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/data/extract_0329G/Live_Trading_System/auto_trade.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/data/home/hmtf000001/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.log /home/hmtf000001/logs/
sudo mv /home/hmtf000001/extract_0329M/extract_0329G/Live_Trading_System/auto_trade.log /home/hmtf000001/logs/
ls /home/hmtf000001/logs/
sudo mv /home/hmtf000001/auto_ai_key.pub /home/hmtf000001/config/
sudo mv /home/hmtf000001/auto_ai_key /home/hmtf000001/config/
sudo mv /home/hmtf000001/auto_ai_ssh_key_bundle.zip /home/hmtf000001/config/
sudo mv /home/hmtf000001/auto_backup.sh /home/hmtf000001/config/
sudo mv /home/hmtf000001/config_file.conf /home/hmtf000001/config/
sudo find /home/hmtf000001/ -name "auto_ai_ssh_key_bundle.zip"
sudo find /home/hmtf000001/ -name "auto_backup.sh"
sudo find /home/hmtf000001/ -name "config_file.conf"
sudo mv /home/hmtf000001/data/auto_ai_ssh_key_bundle.zip /home/hmtf000001/config/
sudo mv /home/hmtf000001/code/auto_backup.sh /home/hmtf000001/config/
ls /home/hmtf000001/code/
ls /home/hmtf000001/backups/
ls /home/hmtf000001/data/
ls /home/hmtf000001/config/
ls /home/hmtf000001/logs/
ls /home/hmtf000001/temp/
sudo find /home/hmtf000001/ -type f
sudo find /home/hmtf000001/ -type f -not -path "/home/hmtf000001/*"
nano --version
crontab -l
crontab -e
crontab -l
nano /home/hmtf000001/code/auto_trade.py
nano /home/hmtf000001/code/auto_trade_script.py
ls -l /home/hmtf000001/code/auto_trade_script.py
sudo chmod u+w /home/hmtf000001/code/auto_trade_script.py
ls /home/hmtf000001/code/
nano /home/hmtf000001/code/auto_trade_script.py
nano /home/hmtf000001/code/auto_trade.py
sudo chmod u+w /home/hmtf000001/code/auto_trade.py
ls -l /home/hmtf000001/code/auto_trade.py
nano /home/hmtf000001/code/auto_trade.py
sudo chmod u+rwx /home/hmtf000001/code/
sudo nano /home/hmtf000001/code/auto_trade.py
sudo nano /home/hmtf000001/code/auto_trade.py
sudo nano /home/hmtf000001/code/auto_trade.py
nano /home/hmtf000001/code/new_test_order.txt
touch /home/hmtf000001/code/new_test_order.txt
ls -ld /home/hmtf000001/code/
sudo chown hmtf000001:hmtf000001 /home/hmtf000001/code/
ls -ld /home/hmtf000001/code/
touch /home/hmtf000001/code/new_test_order.txt
nano /home/hmtf000001/code/new_test_order.txt
check_api_validity()  # 這是用來檢查API金鑰是否有效
nano /home/hmtf000001/code/test_order_script.py
python3 --version
pip3 install requests newsapi-python
sudo apt update
sudo apt install python3-pip
pip3 --version
pip3 install requests newsapi-python
sudo -H pip3 install requests newsapi-python
sudo apt update
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install requests newsapi-python
python auto_trade_test.py
mkdir -p /home/hmtf000001/code/test_orders
nano /home/hmtf000001/code/test_orders/auto_trade_test.py
cd /home/hmtf000001/code/test_orders/
python3 auto_trade_test.py
mkdir -p /home/hmtf000001/code/test_orders
nano /home/hmtf000001/code/test_orders/auto_trade_test.py
mkdir -p /home/hmtf000001/code/test_orders
nano /home/hmtf000001/code/test_orders/auto_trade_test.py
python3 /home/hmtf000001/code/test_orders/auto_trade_test.py
mkdir -p /home/username/code/test_orders
mkdir -p /home/hmtf000001/code/test_orders
sudo chown -R hmtf000001:hmtf000001 /home/hmtf000001/code/test_orders
cd /home/hmtf000001/code/test_orders
nano auto_trade_test.py
python3 /home/hmtf000001/code/test_orders/auto_trade_test.py
pip3 install newsapi-python
source /home/hmtf000001/myenv/bin/activate
pip install newsapi-python
python /home/hmtf000001/code/test_orders/auto_trade_test.py
nano /home/hmtf000001/code/test_orders/auto_trade_test.py
pip install requests newsapi-python
source myenv/bin/activate
pip install requests newsapi-python
python /home/hmtf000001/code/test_orders/auto_trade_test.py
crontab -e
crontab -e
crontab -e
crontab -e
crontab -e
ls /var/spool/cron/crontabs
cat /var/spool/cron/crontabs/<username>
sudo crontab -l
sudo ls /var/spool/cron/crontabs
sudo cat /var/spool/cron/crontabs/hmtf000001
mkdir -p /home/hmtf000001/code/auto_trade
cd /home/hmtf000001/code/auto_trade
nano /home/username/code/auto_trade/auto_trade.py
mkdir -p /home/hmtf000001/code/auto_trade
ls -l /home/hmtf000001/code/auto_trade/
ls -R /
tree /
sudo apt-get update
sudo apt-get install tree
tree /
nano /home/hmtf000001/auto_trading.py
pip install requests
python3 -m venv ~/myenv
source ~/myenv/bin/activate
pip install requests
python /home/hmtf000001/auto_trading.py
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
python /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
crontab -e
chmod +x /home/user/auto_trading.py
chmod +x /home/user/check_api_key.py
chmod +x /home/user/check_market_and_trade.py
chmod +x /home/hmtf000001/auto_trading.py
chmod +x /home/hmtf000001/check_api_key.py
chmod +x /home/hmtf000001/check_market_and_trade.py
ls /home/hmtf000001/auto_trading.py
ls /home/hmtf000001/check_api_key.py
ls /home/hmtf000001/check_market_and_trade.py
chmod +x /home/hmtf000001/auto_trading.py
crontab -e
crontab -l
crontab -e
crontab -e
nano ~/simulate_monday_tasks.sh
nano ~/simulate_monday_tasks.sh
chmod +x ~/simulate_monday_tasks.sh
bash ~/simulate_monday_tasks.sh
source ~/myenv/bin/activate
pip install schedule
pip install newsapi-python
ls /home/hmtf000001/check_api_key.py
nano ~/check_api_key.py
ls /home/hmtf000001/check_market_and_trade.py
nano ~/check_market_and_trade.py
bash ~/simulate_monday_tasks.sh
nano ~/check_api_key.py
nano ~/check_market_and_trade.py
bash ~/simulate_monday_tasks.sh
source ~/myenv/bin/activate
python3 /home/hmtf000001/auto_trading.py
crontab -l
crontab -e
source /home/hmtf000001/myenv/bin/activate
pip install schedule newsapi
source ~/myenv/bin/activate
crontab -e
pip install schedule
pip install newsapi-python
pip install requests
chmod +x /home/hmtf000001/check_api_key.py
chmod +x /home/hmtf000001/check_market_and_trade.py
python3 /home/hmtf000001/check_api_key.py
python3 /home/hmtf000001/check_market_and_trade.py
pip freeze
source ~/myenv/bin/activate
chmod +x /home/hmtf000001/auto_trading.py
chmod +x /home/hmtf000001/check_api_key.py
chmod +x /home/hmtf000001/check_market_and_trade.py
echo "🚀 Running main trading script..."
python3 /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
~/simulate_monday.sh
source ~/myenv/bin/activate
nano ~/simulate_monday.sh
chmod +x ~/simulate_monday.sh
~/simulate_monday.sh
tmux ls
tmux attach-session -t simulate_monday
tmux kill-session -t simulate_monday
tmux new-session -s simulate_monday
bash ~/simulate_monday.sh
tmux attach-session -t simulate_monday
~/simulate_monday.sh
exit
source ~/myenv/bin/activate
sudo apt-get update
sudo apt-get install tmux
tmux
tmux new-session -s simulate_monday
nano ~/simulate_monday.sh
chmod +x ~/simulate_monday.sh
tmux
tmux new-session -s simulate_monday
bash ~/simulate_monday.sh
tmux kill-session -t simulate_monday
tmux new-session -s simulate_monday
bash ~/simulate_monday.sh
unset $TMUX
tmux attach-session -t simulate_monday
tmux ls
tmux ls
tmux attach-session -t simulate_monday
nano /home/hmtf000001/auto_trading.py
nano /home/hmtf000001/auto_trading.py
nano auto_trading.py
cat auto_trading.py
pip install requests
tmux
cd /home/hmtf000001/
unzip Updated_Final_Integrated_Trading_System.zip
cd /home/hmtf000001/
unzip Updated_Final_Integrated_Trading_System0406.zip
ls -l
cat .env
nano .env
nano .env
pip install -r requirements.txt
source ~/myenv/bin/activate
nano test_ig_api.py
python test_ig_api.py
pip install python-dotenv
python test_ig_api.py
nano ~/.env
nano ~/.env
nano test_ig_api.py
python test_ig_api.py
python3 --version
python3 test_ig_api.py
pip install python-dotenv
python3 test_ig_api.py
python3 -m venv myenv
source myenv/bin/activate
pip install python-dotenv
python3 test_ig_api.py
nano ~/.env
source ~/.env
nano ~/.env
source ~/.env
echo $SIM_IG_API_KEY
source ~/myenv/bin/activate
python3 test_ig_api.py
nano ~/.env
nano ~/.env
source ~/.envsource
source ~/.env
source ~/myenv/bin/activate
python3 test_ig_api.py
nano ~/.env
source ~/.env
echo $SIM_IG_API_KEY
nano ~/.env
source ~/.env
echo $SIM_IG_API_KEY
python3 test_ig_api.py
cat ~/.env
cat ~/.env
pwd
ls -l
nano /home/hmtf000001/auto_trading.py
ls -l /home/hmtf000001/auto_trading_system
ls -l /home/hmtf000001/
nano /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
pip install -r requirements.txt
ig-markets-api>=0.3.0
pip install ig-markets-api>=0.3.0
pip install ig-markets-api
git clone https://github.com/ig-python/ig-markets-api.git
cd ig-markets-api
python setup.py install
sudo apt update
sudo apt install git
git clone https://github.com/ig-python/ig-markets-api.git
cd ig-markets-api
python setup.py install
git clone https://github.com/ig-python/ig-markets-api.git
cd ig-markets-api
python setup.py install
source ~/myenv/bin/activate
pip install -r requirements.txt
git clone git@github.com:ig-python/ig-markets-api.git
cat ~/.ssh/id_rsa.pub
source ~/myenv/bin/activate
pip install -r requirements.txt
git clone git@github.com:ig-python/ig-markets-api.git
chmod 600 ~/.ssh/id_rsa
ssh-add ~/.ssh/id_rsa
ssh -T git@github.com
sudo chown -R hmtf000001:hmtf000001 ~/.ssh
sudo chmod 700 ~/.ssh
sudo chmod 600 ~/.ssh/id_rsa
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
ssh -T git@github.com
git clone git@github.com:ig-python/ig-markets-api.git
git clone https://github.com/ig-python/ig-markets-api.git
ssh -T git@github.com
git clone git@github.com:ig-python/ig-markets-api.git
source ~/myenv/bin/activate
pip install -r requirements.txt
pip show requests
pip show pandas
pip show openai
pandas==2.0.3
openai==1.2.3
pip install pandas==2.0.3
pip install openai==1.2.3
pip show pandas
pip show openai
python3 test_ig_api.py
python3 /home/hmtf000001/auto_trading.py
pwd
ls -l
nano auto_trading.py
cat trading_log.txt
which python
pip list
pip install openai pandas requests python-dotenv yfinance binance-connector
source ~/myenv/bin/activate
which pip
pip install --break-system-packages openai pandas requests python-dotenv yfinance binance-connector
pip list
nano /home/hmtf000001/auto_trading.py
python3 /home/hmtf000001/auto_trading.py
cat trading_log.txt
nano /home/hmtf000001/auto_trading.py
python3 /home/hmtf000001/auto_trading.py
cat trading_log.txt
nano /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
source ~/myenv/bin/activate
nano /home/hmtf000001/auto_trading.py
nano ~/.env
nano ~/.env
pip install python-dotenv
nano /home/hmtf000001/auto_trading.py
cd /home/hmtf000001
nano auto_trading.py
nano .env
pip install python-dotenv
crontab -e
sudo apt-get update
sudo apt-get install git
git init
git add .
nano .gitignore
git reset
git add .
nano .gitignore
git reset
git rm --cached -r .cache
git add .
nano .gitignore
git reset
git rm --cached -r .config
git add .
nano .gitignore
git reset
git rm --cached .env*
git add .
nano .gitignore
git rm --cached .local/share/jupyter/*
git add .
nano .gitignore
git rm --cached .python_history
git add .
nano .gitignore
git rm --cached config/auto_ai_key
git add .
echo ".env" >> .gitignore
echo "config/auto_ai_key" >> .gitignore
echo ".local" >> .gitignore
echo ".python_history" >> .gitignore
echo ".cache" >> .gitignore
echo ".config" >> .gitignore
echo "notebook_secret" >> .gitignore
git rm --cached -r .
git add .
nano setup_git.sh
chmod +x setup_git.sh
./setup_git.sh
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global user.name "LUCIFINEL1016"
git config --global user.email "hmtf000001@gmail.com" 
git branch
git checkout -b main
git add .
git commit -m "Initial commit"
git push -u origin main
git status
git add .
cd /home/hmtf000001/
nano .gitignore
git add .gitignore
git commit -m "Initial commit"
git remote -v
git remote add origin https://github.com/LUCIFINEL1016/yourrepository.git
# 将远程仓库添加为 origin
git remote add origin https://github.com/LUCIFINEL1016/Openai_vm_0406.git
# 设置并创建 main 分支
git branch -M main
# 推送到 GitHub
git push -u origin main
git remote add origin https://github.com/LUCIFINEL1016/Openai_vm_0406.git
git remote -v
git remote set-url origin https://github.com/LUCIFINEL1016/Openai_vm_0406.git
git remote -v
git push -u origin main
