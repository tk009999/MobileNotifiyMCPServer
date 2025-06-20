#!/bin/bash

# DC 機器人推播通知器 MCP - 開發環境啟動腳本

set -e

echo "🚀 啟動 DC 機器人推播通知器 MCP 開發環境"

# 檢查是否存在 .env 檔案
if [ ! -f .env ]; then
    echo "📝 建立 .env 檔案..."
    cp env.example .env
    echo "⚠️  請編輯 .env 檔案，填入您的設定值："
    echo "   - DISCORD_BOT_TOKEN"
    echo "   - MCP_SERVER_API_KEY"
    echo "   - DISCORD_BOT_API_URL"
    echo "   - WEBHOOK_SECRET"
    echo "   - JWT_SECRET_KEY"
    exit 1
fi

# 建立必要的目錄
echo "📁 建立必要目錄..."
mkdir -p data logs

# 檢查 Python 虛擬環境
if [ ! -d "venv" ]; then
    echo "🐍 建立 Python 虛擬環境..."
    python3 -m venv venv
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "📦 安裝依賴套件..."
pip install -r requirements.txt

# 選擇啟動模式
echo ""
echo "選擇啟動模式："
echo "1. 只啟動 MCP Server (本地開發)"
echo "2. 只啟動 Discord Bot (本地開發)"
echo "3. 使用 Docker Compose 啟動全部服務"
echo "4. 運行測試"

read -p "請輸入選項 (1-4): " choice

case $choice in
    1)
        echo "🖥️  啟動 MCP Server..."
        export PYTHONPATH=$(pwd)
        python -m src.mcp_server.main
        ;;
    2)
        echo "🤖 啟動 Discord Bot..."
        export PYTHONPATH=$(pwd)
        python -m src.discord_bot.main
        ;;
    3)
        echo "🐳 使用 Docker Compose 啟動..."
        docker-compose up --build
        ;;
    4)
        echo "🧪 運行測試..."
        export PYTHONPATH=$(pwd)
        pytest tests/
        ;;
    *)
        echo "❌ 無效的選項"
        exit 1
        ;;
esac 