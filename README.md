# DC 機器人推播通知器 MCP

讓 Cursor 或 Claude 透過 Discord 機器人實現移動端雙向互動的 MCP 服務器。

## 🚀 快速開始

### 前置需求
- Python 3.9+
- Discord Bot Token
- Discord 應用程式

### 安裝與設置

1. **克隆專案**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **配置環境變數**
```bash
cp .env.example .env
# 編輯 .env 檔案，填入您的 Discord Bot Token 等設定
```

4. **啟動 MCP Server (本地)**
```bash
python -m src.mcp_server.main
```

5. **部署 Discord Bot (雲端)**
```bash
# 詳見部署文檔
```

## 📁 專案結構

```
MobileNotifiyMCPServer/
├── src/
│   ├── mcp_server/          # MCP Server (本地運行)
│   │   ├── main.py         # MCP Server 主程式
│   │   ├── handlers/       # MCP 處理器
│   │   └── models/         # 資料模型
│   ├── discord_bot/        # Discord Bot (雲端運行)
│   │   ├── main.py         # Discord Bot 主程式
│   │   ├── commands/       # Discord 命令
│   │   └── handlers/       # 訊息處理器
│   ├── shared/             # 共用模組
│   │   ├── models.py       # 資料模型
│   │   ├── config.py       # 配置管理
│   │   └── database.py     # 資料庫操作
│   └── utils/              # 工具函數
├── config/                 # 配置檔案
├── docker/                 # Docker 配置
├── tests/                  # 測試檔案
└── docs/                   # 文檔
```

## 🔧 功能特色

- **雙向互動**: AI 可透過 Discord 向您提問，您可直接回覆
- **工作進度通知**: 自動推播工作完成狀態到手機
- **智能過濾**: 根據重要性和時段過濾通知
- **多專案支援**: 同時追蹤多個工作專案

## 📖 使用方式

### MCP Server API

```python
# 發送通知
POST /api/v1/notifications
{
    "type": "milestone",
    "title": "任務完成",
    "content": "已完成資料庫設計",
    "priority": "high"
}
```

### Discord 命令

- `/status` - 查看當前工作狀態
- `/projects` - 列出所有專案
- `/settings` - 配置通知設定

## 🚀 部署

### 本地 MCP Server
```bash
# 開發模式
python -m src.mcp_server.main

# Docker 部署
docker-compose up mcp-server
```

### 雲端 Discord Bot
推薦使用 Railway 或 Heroku 部署 Discord Bot，詳見 [部署指南](docs/deployment.md)。

## 📝 開發狀態

- [x] 專案架構設計
- [x] 基礎 MCP Server
- [x] Discord Bot 核心功能
- [x] 資料庫設計和操作
- [x] API 端點實作
- [x] Docker 容器化配置
- [x] 基本測試架構
- [ ] 通知過濾系統
- [ ] 多專案管理
- [ ] Web 管理介面

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

**專案版本**: v1.1  
**最後更新**: 2024-01-15 