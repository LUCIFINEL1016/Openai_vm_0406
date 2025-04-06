#!/bin/bash

# 檢查參數
if [ "$1" == "live" ]; then
  export SIM_IG_API_KEY="2181c539a32c9f60e1119673c96598eaf2be45e3"
  export SIM_IG_USERNAME="Lucifinel1016"
  export SIM_IG_PASSWORD="S06109811s"
  echo "✅ 已切換至 LIVE（主用）API Key 組合"

elif [ "$1" == "backup" ]; then
  export SIM_IG_API_KEY="a15f21a2886f0532d5d324ba6701289275524d23"
  export SIM_IG_USERNAME="Lucifinel1016"
  export SIM_IG_PASSWORD="S11223344s"
  echo "🔁 已切換至 BACKUP（備用）API Key 組合"

else
  echo "❌ 請輸入參數：live 或 backup"
  echo "用法：./switch_key.sh live"
  exit 1
fi
