# Discord Bot 部署指南

## 📋 目錄
1. [Discord Bot 設置](#discord-bot-設置)
2. [環境變數配置](#環境變數配置)
3. [本地測試](#本地測試)
4. [雲端部署](#雲端部署)
5. [監控和維護](#監控和維護)

## 🤖 Discord Bot 設置

### 步驟 1: 建立 Discord 應用程式

1. **前往 Discord Developer Portal**
   - 訪問 https://discord.com/developers/applications
   - 使用你的 Discord 帳號登入

2. **建立新應用程式**
   ```
   點擊 "New Application" → 輸入應用程式名稱 → "Create"
   ```

3. **配置應用程式資訊**
   - **Name**: `DC 機器人推播通知器`
   - **Description**: `讓 Cursor 或 Claude 透過 Discord 實現移動端雙向互動的通知機器人`
   - **App Icon**: 上傳機器人頭像（可選）

### 步驟 2: 建立 Bot

1. **進入 Bot 設置**
   ```
   左側選單 → "Bot" → "Add Bot" → "Yes, do it!"
   ```

2. **配置 Bot 設定**
   - **Username**: `MCP-Notifier` (或你喜歡的名稱)
   - **Public Bot**: ❌ 關閉 (建議設為私人)
   - **Requires OAuth2 Code Grant**: ❌ 關閉
   - **Presence Intent**: ✅ 開啟
   - **Server Members Intent**: ✅ 開啟
   - **Message Content Intent**: ✅ 開啟

3. **複製 Bot Token**
   ```
   點擊 "Reset Token" → "Copy" → 安全保存此 Token
   ```
   ⚠️ **重要**: Token 只會顯示一次，請立即複製並妥善保存！

### 步驟 3: 設置 OAuth2 權限

1. **進入 OAuth2 設置**
   ```
   左側選單 → "OAuth2" → "URL Generator"
   ```

2. **選擇 Scopes**
   - ✅ `bot`
   - ✅ `applications.commands`

3. **選擇 Bot Permissions**
   - ✅ `Send Messages` (發送訊息)
   - ✅ `Use Slash Commands` (使用斜線命令)
   - ✅ `Read Message History` (讀取訊息歷史)
   - ✅ `Add Reactions` (添加反應)
   - ✅ `Embed Links` (嵌入連結)

4. **生成邀請連結**
   ```
   複製底部生成的 URL → 在瀏覽器中開啟 → 選擇伺服器 → "授權"
   ```

## ⚙️ 環境變數配置

### 建立環境變數檔案

```bash
# 複製範例檔案
cp env.example .env

# 編輯環境變數
nano .env  # 或使用你喜歡的編輯器
```

### 必要的環境變數

```env
# Discord Bot 設定
DISCORD_BOT_TOKEN=你的_discord_bot_token
DISCORD_GUILD_ID=你的_discord_伺服器_id

# MCP Server 設定
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
MCP_SERVER_API_KEY=生成一個安全的API金鑰

# 資料庫設定
DATABASE_URL=sqlite:///./mcp_notifications.db

# 通信設定
DISCORD_BOT_API_URL=https://你的機器人部署網址.com
WEBHOOK_SECRET=生成一個安全的webhook密鑰

# 日誌設定
LOG_LEVEL=INFO
LOG_FILE=./logs/discord_bot.log
```

### 獲取 Discord Guild ID

1. **啟用開發者模式**
   ```
   Discord → 設定 → 進階 → 開發者模式 ✅
   ```

2. **獲取伺服器 ID**
   ```
   右鍵點擊伺服器名稱 → "複製伺服器 ID"
   ```

## 🧪 本地測試

### 安裝依賴

```bash
# 確保在專案根目錄
cd MobileNotifiyMCPServer

# 安裝 Python 依賴
pip install -r requirements.txt
```

### 啟動 Discord Bot

```bash
# 方法 1: 直接執行
python -m src.discord_bot.main

# 方法 2: 使用開發腳本
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh discord-bot
```

### 測試機器人功能

1. **檢查機器人狀態**
   ```
   在 Discord 中輸入: /status
   ```

2. **測試幫助命令**
   ```
   在 Discord 中輸入: /help
   ```

3. **查看專案列表**
   ```
   在 Discord 中輸入: /projects
   ```

## ☁️ 雲端部署

### 選項 1: Railway 部署 (推薦)

1. **準備 Railway 帳號**
   - 訪問 https://railway.app
   - 使用 GitHub 帳號登入

2. **建立新專案**
   ```bash
   # 安裝 Railway CLI
   npm install -g @railway/cli
   
   # 登入 Railway
   railway login
   
   # 初始化專案
   railway init
   ```

3. **配置環境變數**
   ```bash
   # 設置環境變數
   railway variables set DISCORD_BOT_TOKEN=你的token
   railway variables set DISCORD_GUILD_ID=你的guild_id
   railway variables set MCP_SERVER_HOST=你的mcp_server網址
   railway variables set MCP_SERVER_PORT=8000
   railway variables set MCP_SERVER_API_KEY=你的api_key
   railway variables set WEBHOOK_SECRET=你的webhook_secret
   ```

4. **部署**
   ```bash
   # 部署 Discord Bot
   railway up --service discord-bot
   ```

### 選項 2: Heroku 部署

1. **準備 Heroku 帳號**
   - 訪問 https://heroku.com
   - 建立免費帳號

2. **安裝 Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # 登入
   heroku login
   ```

3. **建立 Heroku 應用程式**
   ```bash
   # 建立應用程式
   heroku create your-discord-bot-name
   
   # 設置環境變數
   heroku config:set DISCORD_BOT_TOKEN=你的token
   heroku config:set DISCORD_GUILD_ID=你的guild_id
   heroku config:set MCP_SERVER_HOST=你的mcp_server網址
   heroku config:set MCP_SERVER_PORT=8000
   heroku config:set MCP_SERVER_API_KEY=你的api_key
   heroku config:set WEBHOOK_SECRET=你的webhook_secret
   ```

4. **部署**
   ```bash
   # 推送到 Heroku
   git push heroku main
   ```

### 選項 3: Docker 部署

1. **建立 Docker 映像**
   ```bash
   # 建立 Discord Bot 映像
   docker build -f docker/Dockerfile.discord-bot -t discord-bot .
   ```

2. **執行容器**
   ```bash
   # 使用 docker-compose
   docker-compose up discord-bot
   
   # 或直接執行
   docker run -d \
     --name discord-bot \
     --env-file .env \
     -p 8080:8080 \
     discord-bot
   ```

## 📊 監控和維護

### 檢查部署狀態

```bash
# Railway
railway status

# Heroku
heroku ps

# Docker
docker ps
docker logs discord-bot
```

### 查看日誌

```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# Docker
docker logs -f discord-bot
```

### 健康檢查

機器人提供了健康檢查端點：

```bash
# 檢查機器人狀態
curl https://你的機器人網址.com/health

# 預期回應
{
  "status": "healthy",
  "discord_bot_status": "connected",
  "mcp_server_connection": "healthy",
  "uptime": "2h 30m 15s"
}
```

## 🔧 故障排除

### 常見問題

1. **Bot Token 無效**
   ```
   錯誤: discord.errors.LoginFailure
   解決: 檢查 DISCORD_BOT_TOKEN 是否正確
   ```

2. **權限不足**
   ```
   錯誤: discord.errors.Forbidden
   解決: 檢查機器人權限設置
   ```

3. **MCP Server 連接失敗**
   ```
   錯誤: httpx.ConnectError
   解決: 檢查 MCP_SERVER_HOST 和 MCP_SERVER_PORT
   ```

### 除錯模式

```bash
# 啟用除錯日誌
export LOG_LEVEL=DEBUG
python -m src.discord_bot.main
```

## 🚀 下一步

部署完成後，你可以：

1. **測試通知功能**: 啟動 MCP Server 並測試通知推送
2. **配置通知規則**: 設置通知過濾和時間規則
3. **監控系統狀態**: 設置監控告警
4. **擴展功能**: 添加更多 Discord 命令

## 📞 支援

如果遇到問題，請：

1. 檢查日誌檔案
2. 確認環境變數設置
3. 查看 [故障排除指南](#故障排除)
4. 提交 Issue 到 GitHub 儲存庫

---

**部署指南版本**: v1.0  
**最後更新**: 2024-01-15 