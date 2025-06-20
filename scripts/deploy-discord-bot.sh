#!/bin/bash

# Discord Bot 快速部署腳本
# 使用方式: ./scripts/deploy-discord-bot.sh [platform]
# 平台選項: railway, heroku, docker

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查必要工具
check_requirements() {
    log_info "檢查必要工具..."
    
    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安裝"
        exit 1
    fi
    
    # 檢查 pip
    if ! command -v pip &> /dev/null; then
        log_error "pip 未安裝"
        exit 1
    fi
    
    # 檢查 git
    if ! command -v git &> /dev/null; then
        log_error "git 未安裝"
        exit 1
    fi
    
    log_success "所有必要工具已安裝"
}

# 檢查環境變數
check_env_vars() {
    log_info "檢查環境變數..."
    
    if [ ! -f ".env" ]; then
        log_warning ".env 檔案不存在，從範例建立..."
        cp env.example .env
        log_warning "請編輯 .env 檔案並設置必要的環境變數"
        log_warning "特別是 DISCORD_BOT_TOKEN 和 DISCORD_GUILD_ID"
        read -p "按 Enter 繼續..."
    fi
    
    # 檢查關鍵環境變數
    source .env
    
    if [ -z "$DISCORD_BOT_TOKEN" ] || [ "$DISCORD_BOT_TOKEN" = "your_discord_bot_token_here" ]; then
        log_error "DISCORD_BOT_TOKEN 未設置"
        log_error "請在 .env 檔案中設置正確的 Discord Bot Token"
        exit 1
    fi
    
    if [ -z "$DISCORD_GUILD_ID" ] || [ "$DISCORD_GUILD_ID" = "your_discord_guild_id_here" ]; then
        log_error "DISCORD_GUILD_ID 未設置"
        log_error "請在 .env 檔案中設置正確的 Discord Guild ID"
        exit 1
    fi
    
    log_success "環境變數檢查完成"
}

# 安裝依賴
install_dependencies() {
    log_info "安裝 Python 依賴..."
    pip install -r requirements.txt
    log_success "依賴安裝完成"
}

# 本地測試
test_locally() {
    log_info "進行本地測試..."
    
    # 建立日誌目錄
    mkdir -p logs
    
    # 設置環境變數
    export PYTHONPATH=$(pwd)
    
    # 測試導入
    python3 -c "
import sys
sys.path.append('.')
try:
    from src.discord_bot.main import bot
    print('✅ Discord Bot 模組導入成功')
except Exception as e:
    print(f'❌ Discord Bot 模組導入失敗: {e}')
    sys.exit(1)
"
    
    log_success "本地測試通過"
}

# Railway 部署
deploy_railway() {
    log_info "準備 Railway 部署..."
    
    # 檢查 Railway CLI
    if ! command -v railway &> /dev/null; then
        log_warning "Railway CLI 未安裝，正在安裝..."
        npm install -g @railway/cli
    fi
    
    # 登入檢查
    if ! railway whoami &> /dev/null; then
        log_info "請登入 Railway..."
        railway login
    fi
    
    # 初始化專案
    if [ ! -f "railway.json" ]; then
        log_info "初始化 Railway 專案..."
        railway init
    fi
    
    # 設置環境變數
    log_info "設置環境變數..."
    source .env
    
    railway variables set DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN"
    railway variables set DISCORD_GUILD_ID="$DISCORD_GUILD_ID"
    railway variables set MCP_SERVER_HOST="$MCP_SERVER_HOST"
    railway variables set MCP_SERVER_PORT="$MCP_SERVER_PORT"
    railway variables set MCP_SERVER_API_KEY="$MCP_SERVER_API_KEY"
    railway variables set WEBHOOK_SECRET="$WEBHOOK_SECRET"
    railway variables set LOG_LEVEL="$LOG_LEVEL"
    
    # 部署
    log_info "開始部署到 Railway..."
    railway up
    
    log_success "Railway 部署完成！"
    log_info "查看部署狀態: railway status"
    log_info "查看日誌: railway logs"
}

# Heroku 部署
deploy_heroku() {
    log_info "準備 Heroku 部署..."
    
    # 檢查 Heroku CLI
    if ! command -v heroku &> /dev/null; then
        log_error "Heroku CLI 未安裝"
        log_info "請訪問 https://devcenter.heroku.com/articles/heroku-cli 安裝"
        exit 1
    fi
    
    # 登入檢查
    if ! heroku whoami &> /dev/null; then
        log_info "請登入 Heroku..."
        heroku login
    fi
    
    # 建立應用程式
    read -p "請輸入 Heroku 應用程式名稱: " app_name
    
    if [ -z "$app_name" ]; then
        log_error "應用程式名稱不能為空"
        exit 1
    fi
    
    log_info "建立 Heroku 應用程式: $app_name"
    heroku create "$app_name" || log_warning "應用程式可能已存在"
    
    # 設置環境變數
    log_info "設置環境變數..."
    source .env
    
    heroku config:set DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN" -a "$app_name"
    heroku config:set DISCORD_GUILD_ID="$DISCORD_GUILD_ID" -a "$app_name"
    heroku config:set MCP_SERVER_HOST="$MCP_SERVER_HOST" -a "$app_name"
    heroku config:set MCP_SERVER_PORT="$MCP_SERVER_PORT" -a "$app_name"
    heroku config:set MCP_SERVER_API_KEY="$MCP_SERVER_API_KEY" -a "$app_name"
    heroku config:set WEBHOOK_SECRET="$WEBHOOK_SECRET" -a "$app_name"
    heroku config:set LOG_LEVEL="$LOG_LEVEL" -a "$app_name"
    
    # 建立 Procfile
    echo "worker: python -m src.discord_bot.main" > Procfile
    
    # 部署
    log_info "開始部署到 Heroku..."
    git add Procfile
    git commit -m "Add Procfile for Heroku deployment" || true
    
    heroku git:remote -a "$app_name"
    git push heroku main
    
    # 啟動 worker
    heroku ps:scale worker=1 -a "$app_name"
    
    log_success "Heroku 部署完成！"
    log_info "查看日誌: heroku logs --tail -a $app_name"
}

# Docker 部署
deploy_docker() {
    log_info "準備 Docker 部署..."
    
    # 檢查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝"
        exit 1
    fi
    
    # 建立 Docker 映像
    log_info "建立 Docker 映像..."
    docker build -f docker/Dockerfile.discord-bot -t discord-bot .
    
    # 停止舊容器
    docker stop discord-bot 2>/dev/null || true
    docker rm discord-bot 2>/dev/null || true
    
    # 啟動新容器
    log_info "啟動 Discord Bot 容器..."
    docker run -d \
        --name discord-bot \
        --env-file .env \
        --restart unless-stopped \
        -p 8080:8080 \
        discord-bot
    
    log_success "Docker 部署完成！"
    log_info "查看容器狀態: docker ps"
    log_info "查看日誌: docker logs -f discord-bot"
}

# 主函數
main() {
    echo "🤖 Discord Bot 部署腳本"
    echo "========================="
    
    PLATFORM=${1:-""}
    
    if [ -z "$PLATFORM" ]; then
        echo "使用方式: $0 <platform>"
        echo "平台選項:"
        echo "  railway  - 部署到 Railway (推薦)"
        echo "  heroku   - 部署到 Heroku"
        echo "  docker   - 本地 Docker 部署"
        echo "  test     - 僅進行本地測試"
        exit 1
    fi
    
    # 執行檢查
    check_requirements
    check_env_vars
    install_dependencies
    
    # 根據平台部署
    case $PLATFORM in
        "railway")
            test_locally
            deploy_railway
            ;;
        "heroku")
            test_locally
            deploy_heroku
            ;;
        "docker")
            test_locally
            deploy_docker
            ;;
        "test")
            test_locally
            log_success "本地測試完成！"
            log_info "要啟動 Discord Bot，執行: python -m src.discord_bot.main"
            ;;
        *)
            log_error "不支援的平台: $PLATFORM"
            exit 1
            ;;
    esac
    
    log_success "部署完成！ 🎉"
}

# 執行主函數
main "$@" 