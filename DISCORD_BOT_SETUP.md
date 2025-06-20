# 🤖 Discord Bot 快速設置指南

## 📋 設置清單

在開始部署之前，請確保完成以下步驟：

### ✅ 1. Discord Bot 建立
- [ ] 在 Discord Developer Portal 建立應用程式
- [ ] 建立 Bot 並複製 Token
- [ ] 設置 Bot 權限和 Intents
- [ ] 邀請 Bot 到你的 Discord 伺服器
- [ ] 獲取 Discord Guild ID

### ✅ 2. 環境設置
- [ ] 複製並編輯 `.env` 檔案
- [ ] 設置 Discord Bot Token
- [ ] 設置 Discord Guild ID
- [ ] 配置其他必要環境變數

### ✅ 3. 選擇部署平台
- [ ] Railway (推薦，免費額度充足)
- [ ] Heroku (經典選擇)
- [ ] Docker (本地部署)

---

## 🚀 一鍵部署

### Railway 部署 (推薦)
```bash
# 快速部署到 Railway
./scripts/deploy-discord-bot.sh railway
```

### Heroku 部署
```bash
# 部署到 Heroku
./scripts/deploy-discord-bot.sh heroku
```

### Docker 本地部署
```bash
# Docker 容器部署
./scripts/deploy-discord-bot.sh docker
```

### 本地測試
```bash
# 僅進行本地測試
./scripts/deploy-discord-bot.sh test
```

---

## 📝 詳細步驟

如果你需要手動設置，請參考 [完整部署指南](docs/DISCORD_BOT_DEPLOYMENT.md)。

---

## ⚡ 快速開始

### 1. 建立 Discord Bot

1. **前往 Discord Developer Portal**
   - 訪問: https://discord.com/developers/applications
   - 登入你的 Discord 帳號

2. **建立新應用程式**
   - 點擊 "New Application"
   - 輸入名稱: `DC 機器人推播通知器`
   - 點擊 "Create"

3. **建立 Bot**
   - 左側選單 → "Bot"
   - 點擊 "Add Bot" → "Yes, do it!"
   - 複製 Bot Token (重要！)

4. **設置權限**
   - 在 Bot 設定頁面：
     - ✅ Message Content Intent
     - ✅ Server Members Intent
     - ✅ Presence Intent

5. **邀請 Bot**
   - 左側選單 → "OAuth2" → "URL Generator"
   - Scopes: `bot` + `applications.commands`
   - Bot Permissions: 
     - ✅ Send Messages
     - ✅ Use Slash Commands
     - ✅ Read Message History
     - ✅ Add Reactions
     - ✅ Embed Links
   - 複製生成的 URL 並在瀏覽器中打開
   - 選擇你的 Discord 伺服器並授權

### 2. 獲取 Guild ID

1. **啟用開發者模式**
   - Discord → 設定 → 進階 → 開發者模式 ✅

2. **複製伺服器 ID**
   - 右鍵點擊你的伺服器名稱
   - 選擇 "複製伺服器 ID"

### 3. 設置環境變數

```bash
# 複製環境變數範例檔案
cp env.example .env

# 編輯 .env 檔案
nano .env
```

**必須設置的變數：**
```env
# Discord Bot 設定
DISCORD_BOT_TOKEN=你的_discord_bot_token
DISCORD_GUILD_ID=你的_discord_伺服器_id

# MCP Server 設定 (如果本地運行)
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
MCP_SERVER_API_KEY=your_secure_api_key_here

# 其他設定
WEBHOOK_SECRET=your_secure_webhook_secret_here
LOG_LEVEL=INFO
```

### 4. 一鍵部署

```bash
# 部署到 Railway (推薦)
./scripts/deploy-discord-bot.sh railway

# 或者先測試
./scripts/deploy-discord-bot.sh test
```

---

## 🔧 驗證部署

部署完成後，在你的 Discord 伺服器中測試：

```
/status    - 檢查系統狀態
/help      - 查看幫助資訊
/projects  - 列出專案
```

如果命令正常工作，表示部署成功！ 🎉

---

## 📞 需要幫助？

- 📖 [完整部署指南](docs/DISCORD_BOT_DEPLOYMENT.md)
- 🐛 [故障排除](docs/DISCORD_BOT_DEPLOYMENT.md#故障排除)
- 💬 [GitHub Issues](https://github.com/tk009999/MobileNotifiyMCPServer/issues)

---

**快速設置指南版本**: v1.0  
**最後更新**: 2024-01-15 