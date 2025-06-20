# DC 機器人推播通知器 MCP

[![Languages](https://img.shields.io/badge/Languages-7-blue.svg)](#languages)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](https://github.com/tk009999/MobileNotifiyMCPServer/releases)

## 🌍 Languages / 語言選擇

- [🇹🇼 繁體中文](#繁體中文)
- [🇺🇸 English](#english)
- [🇯🇵 日本語](#日本語)
- [🇫🇷 Français](#français)
- [🇩🇪 Deutsch](#deutsch)
- [🇪🇸 Español](#español)
- [🇸🇦 العربية](#العربية)

---

## 繁體中文

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

**專案版本**: v2.0  
**最後更新**: 2024-01-15

---

## English

A MCP server that enables seamless mobile interaction between Cursor/Claude and users through Discord bot bidirectional communication.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Discord Bot Token
- Discord Application

### Installation & Setup

1. **Clone the Project**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment Variables**
```bash
cp env.example .env
# Edit .env file and fill in your Discord Bot Token and other settings
```

4. **Start MCP Server (Local)**
```bash
python -m src.mcp_server.main
```

5. **Deploy Discord Bot (Cloud)**
```bash
# See deployment documentation
```

## 📁 Project Structure

```
MobileNotifiyMCPServer/
├── src/
│   ├── mcp_server/          # MCP Server (runs locally)
│   │   ├── main.py         # MCP Server main program
│   │   ├── handlers/       # MCP handlers
│   │   └── models/         # Data models
│   ├── discord_bot/        # Discord Bot (runs in cloud)
│   │   ├── main.py         # Discord Bot main program
│   │   ├── commands/       # Discord commands
│   │   └── handlers/       # Message handlers
│   ├── shared/             # Shared modules
│   │   ├── models.py       # Data models
│   │   ├── config.py       # Configuration management
│   │   └── database.py     # Database operations
│   └── utils/              # Utility functions
├── config/                 # Configuration files
├── docker/                 # Docker configurations
├── tests/                  # Test files
└── docs/                   # Documentation
```

## 🔧 Features

- **Bidirectional Interaction**: AI can ask questions via Discord, you can reply directly
- **Work Progress Notifications**: Automatic push notifications of work completion status to mobile
- **Smart Filtering**: Filter notifications based on importance and time slots
- **Multi-Project Support**: Track multiple work projects simultaneously

## 📖 Usage

### MCP Server API

```python
# Send notification
POST /api/v1/notifications
{
    "type": "milestone",
    "title": "Task Completed",
    "content": "Database design completed",
    "priority": "high"
}
```

### Discord Commands

- `/status` - View current system status
- `/projects` - List all projects
- `/settings` - Configure notification settings

## 🚀 Deployment

### Local MCP Server
```bash
# Development mode
python -m src.mcp_server.main

# Docker deployment
docker-compose up mcp-server
```

### Cloud Discord Bot
Recommended deployment on Railway or Heroku for Discord Bot. See [Deployment Guide](docs/deployment.md).

## 📝 Development Status

- [x] Project architecture design
- [x] Basic MCP Server
- [x] Discord Bot core functionality
- [x] Database design and operations
- [x] API endpoint implementation
- [x] Docker containerization configuration
- [x] Basic testing framework
- [ ] Notification filtering system
- [ ] Multi-project management
- [ ] Web management interface

## 📄 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

**Project Version**: v2.0  
**Last Updated**: 2024-01-15

---

## 日本語

Cursor または Claude が Discord ボットを通じてモバイル端末で双方向のやり取りを実現する MCP サーバー。

## 🚀 クイックスタート

### 前提条件
- Python 3.9+
- Discord Bot Token
- Discord アプリケーション

### インストールとセットアップ

1. **プロジェクトのクローン**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

3. **環境変数の設定**
```bash
cp env.example .env
# .env ファイルを編集し、Discord Bot Token などの設定を入力
```

4. **MCP Server の起動（ローカル）**
```bash
python -m src.mcp_server.main
```

5. **Discord Bot のデプロイ（クラウド）**
```bash
# デプロイメントドキュメントを参照
```

## 🔧 機能

- **双方向インタラクション**: AI が Discord 経由で質問し、直接返答可能
- **作業進捗通知**: 作業完了状況をモバイル端末に自動プッシュ通知
- **スマートフィルタリング**: 重要度と時間帯に基づく通知フィルタリング
- **マルチプロジェクトサポート**: 複数の作業プロジェクトを同時追跡

## 📖 使用方法

### Discord コマンド

- `/status` - 現在のシステム状態を表示
- `/projects` - 全プロジェクトを一覧表示
- `/settings` - 通知設定を構成

## 📝 開発状況

- [x] プロジェクトアーキテクチャ設計
- [x] 基本 MCP Server
- [x] Discord Bot コア機能
- [x] データベース設計と操作
- [x] API エンドポイント実装
- [x] Docker コンテナ化設定
- [x] 基本テストフレームワーク
- [ ] 通知フィルタリングシステム
- [ ] マルチプロジェクト管理
- [ ] Web 管理インターフェース

---

**プロジェクトバージョン**: v2.0  
**最終更新**: 2024-01-15

---

## Français

Un serveur MCP qui permet une interaction mobile transparente entre Cursor/Claude et les utilisateurs grâce à la communication bidirectionnelle du bot Discord.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.9+
- Discord Bot Token
- Application Discord

### Installation et Configuration

1. **Cloner le Projet**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **Installer les Dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les Variables d'Environnement**
```bash
cp env.example .env
# Éditer le fichier .env et remplir votre Discord Bot Token et autres paramètres
```

## 🔧 Fonctionnalités

- **Interaction Bidirectionnelle**: L'IA peut poser des questions via Discord, vous pouvez répondre directement
- **Notifications de Progression**: Notifications push automatiques du statut d'achèvement du travail vers mobile
- **Filtrage Intelligent**: Filtrer les notifications basé sur l'importance et les créneaux horaires
- **Support Multi-Projets**: Suivre plusieurs projets de travail simultanément

## 📖 Utilisation

### Commandes Discord

- `/status` - Voir le statut actuel du système
- `/projects` - Lister tous les projets
- `/settings` - Configurer les paramètres de notification

## 📝 Statut de Développement

- [x] Conception de l'architecture du projet
- [x] Serveur MCP de base
- [x] Fonctionnalité centrale du bot Discord
- [x] Conception et opérations de base de données
- [x] Implémentation des points de terminaison API
- [x] Configuration de conteneurisation Docker
- [x] Framework de test de base
- [ ] Système de filtrage des notifications
- [ ] Gestion multi-projets
- [ ] Interface de gestion web

---

**Version du Projet**: v2.0  
**Dernière Mise à Jour**: 2024-01-15

---

## Deutsch

Ein MCP-Server, der nahtlose mobile Interaktion zwischen Cursor/Claude und Benutzern durch bidirektionale Discord-Bot-Kommunikation ermöglicht.

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.9+
- Discord Bot Token
- Discord Anwendung

### Installation & Einrichtung

1. **Projekt Klonen**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **Abhängigkeiten Installieren**
```bash
pip install -r requirements.txt
```

3. **Umgebungsvariablen Konfigurieren**
```bash
cp env.example .env
# .env Datei bearbeiten und Discord Bot Token sowie andere Einstellungen ausfüllen
```

## 🔧 Features

- **Bidirektionale Interaktion**: KI kann Fragen über Discord stellen, Sie können direkt antworten
- **Arbeitsfortschritt-Benachrichtigungen**: Automatische Push-Benachrichtigungen des Arbeitsabschlussstatus an mobile Geräte
- **Intelligente Filterung**: Benachrichtigungen basierend auf Wichtigkeit und Zeitfenstern filtern
- **Multi-Projekt-Unterstützung**: Mehrere Arbeitsprojekte gleichzeitig verfolgen

## 📖 Verwendung

### Discord Befehle

- `/status` - Aktuellen Systemstatus anzeigen
- `/projects` - Alle Projekte auflisten
- `/settings` - Benachrichtigungseinstellungen konfigurieren

## 📝 Entwicklungsstatus

- [x] Projektarchitektur-Design
- [x] Basis MCP Server
- [x] Discord Bot Kernfunktionalität
- [x] Datenbank-Design und -Operationen
- [x] API-Endpunkt-Implementierung
- [x] Docker-Containerisierung-Konfiguration
- [x] Basis-Test-Framework
- [ ] Benachrichtigungsfiltersystem
- [ ] Multi-Projekt-Management
- [ ] Web-Management-Interface

---

**Projektversion**: v2.0  
**Letzte Aktualisierung**: 2024-01-15

---

## Español

Un servidor MCP que permite interacción móvil perfecta entre Cursor/Claude y usuarios a través de comunicación bidireccional del bot de Discord.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.9+
- Discord Bot Token
- Aplicación Discord

### Instalación y Configuración

1. **Clonar el Proyecto**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar Variables de Entorno**
```bash
cp env.example .env
# Editar archivo .env y completar tu Discord Bot Token y otras configuraciones
```

## 🔧 Características

- **Interacción Bidireccional**: La IA puede hacer preguntas vía Discord, puedes responder directamente
- **Notificaciones de Progreso de Trabajo**: Notificaciones push automáticas del estado de finalización del trabajo al móvil
- **Filtrado Inteligente**: Filtrar notificaciones basado en importancia y franjas horarias
- **Soporte Multi-Proyecto**: Rastrear múltiples proyectos de trabajo simultáneamente

## 📖 Uso

### Comandos de Discord

- `/status` - Ver estado actual del sistema
- `/projects` - Listar todos los proyectos
- `/settings` - Configurar ajustes de notificación

## 📝 Estado de Desarrollo

- [x] Diseño de arquitectura del proyecto
- [x] Servidor MCP básico
- [x] Funcionalidad central del bot de Discord
- [x] Diseño y operaciones de base de datos
- [x] Implementación de endpoints API
- [x] Configuración de contenerización Docker
- [x] Framework de pruebas básico
- [ ] Sistema de filtrado de notificaciones
- [ ] Gestión multi-proyecto
- [ ] Interfaz de gestión web

---

**Versión del Proyecto**: v2.0  
**Última Actualización**: 2024-01-15

---

## العربية

خادم MCP يمكّن التفاعل المحمول السلس بين Cursor/Claude والمستخدمين من خلال التواصل ثنائي الاتجاه لبوت Discord.

## 🚀 البدء السريع

### المتطلبات المسبقة
- Python 3.9+
- Discord Bot Token
- تطبيق Discord

### التثبيت والإعداد

1. **استنساخ المشروع**
```bash
git clone https://github.com/tk009999/MobileNotifiyMCPServer.git
cd MobileNotifiyMCPServer
```

2. **تثبيت التبعيات**
```bash
pip install -r requirements.txt
```

3. **تكوين متغيرات البيئة**
```bash
cp env.example .env
# قم بتحرير ملف .env وملء Discord Bot Token والإعدادات الأخرى
```

## 🔧 الميزات

- **التفاعل ثنائي الاتجاه**: يمكن للذكاء الاصطناعي طرح الأسئلة عبر Discord، ويمكنك الرد مباشرة
- **إشعارات تقدم العمل**: إشعارات تلقائية لحالة إنجاز العمل إلى الهاتف المحمول
- **التصفية الذكية**: تصفية الإشعارات بناءً على الأهمية والفترات الزمنية
- **دعم متعدد المشاريع**: تتبع عدة مشاريع عمل في وقت واحد

## 📖 الاستخدام

### أوامر Discord

- `/status` - عرض حالة النظام الحالية
- `/projects` - إدراج جميع المشاريع
- `/settings` - تكوين إعدادات الإشعارات

## 📝 حالة التطوير

- [x] تصميم بنية المشروع
- [x] خادم MCP الأساسي
- [x] الوظائف الأساسية لبوت Discord
- [x] تصميم وعمليات قاعدة البيانات
- [x] تنفيذ نقاط النهاية API
- [x] تكوين الحاويات Docker
- [x] إطار اختبار أساسي
- [ ] نظام تصفية الإشعارات
- [ ] إدارة متعددة المشاريع
- [ ] واجهة إدارة الويب

---

**إصدار المشروع**: v2.0  
**آخر تحديث**: 2024-01-15 