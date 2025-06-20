"""
配置管理模組
統一管理系統配置和環境變數
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """系統設定類別"""
    
    # Discord Bot 設定
    discord_bot_token: str = Field(..., env="DISCORD_BOT_TOKEN")
    discord_guild_id: Optional[str] = Field(None, env="DISCORD_GUILD_ID")
    
    # MCP Server 設定
    mcp_server_host: str = Field("localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(8000, env="MCP_SERVER_PORT")
    mcp_server_api_key: str = Field(..., env="MCP_SERVER_API_KEY")
    
    # 資料庫設定
    database_url: str = Field("sqlite:///./mcp_notifications.db", env="DATABASE_URL")
    
    # 通信設定
    discord_bot_api_url: str = Field(..., env="DISCORD_BOT_API_URL")
    webhook_secret: str = Field(..., env="WEBHOOK_SECRET")
    
    # 日誌設定
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/mcp_server.log", env="LOG_FILE")
    
    # 通知設定
    default_notification_priority: str = Field("medium", env="DEFAULT_NOTIFICATION_PRIORITY")
    quiet_hours_start: str = Field("22:00", env="QUIET_HOURS_START")
    quiet_hours_end: str = Field("08:00", env="QUIET_HOURS_END")
    
    # 安全設定
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    cors_allowed_origins: List[str] = Field(
        ["http://localhost:3000"],
        env="CORS_ALLOWED_ORIGINS"
    )
    
    # 系統設定
    max_notification_retry: int = Field(3, env="MAX_NOTIFICATION_RETRY")
    notification_timeout: int = Field(30, env="NOTIFICATION_TIMEOUT")
    health_check_interval: int = Field(60, env="HEALTH_CHECK_INTERVAL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_cors_origins(self) -> List[str]:
        """獲取 CORS 允許的來源列表"""
        if isinstance(self.cors_allowed_origins, str):
            return [origin.strip() for origin in self.cors_allowed_origins.split(",")]
        return self.cors_allowed_origins


class MCPServerConfig:
    """MCP Server 特定配置"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    @property
    def server_url(self) -> str:
        """獲取 MCP Server 完整 URL"""
        return f"http://{self.settings.mcp_server_host}:{self.settings.mcp_server_port}"
    
    @property
    def api_headers(self) -> dict:
        """獲取 API 請求標頭"""
        return {
            "Authorization": f"Bearer {self.settings.mcp_server_api_key}",
            "Content-Type": "application/json"
        }


class DiscordBotConfig:
    """Discord Bot 特定配置"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    @property
    def bot_intents(self):
        """獲取 Discord Bot 所需權限"""
        import discord
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        intents.dm_messages = True
        return intents
    
    @property
    def command_prefix(self) -> str:
        """獲取命令前綴"""
        return "/"


class DatabaseConfig:
    """資料庫配置"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    @property
    def engine_kwargs(self) -> dict:
        """獲取資料庫引擎參數"""
        if "sqlite" in self.settings.database_url:
            return {
                "echo": self.settings.log_level.upper() == "DEBUG",
                "pool_pre_ping": True,
                "connect_args": {"check_same_thread": False}
            }
        else:
            return {
                "echo": self.settings.log_level.upper() == "DEBUG",
                "pool_pre_ping": True,
                "pool_size": 10,
                "max_overflow": 20
            }


# 全域設定實例
settings = Settings()
mcp_config = MCPServerConfig(settings)
discord_config = DiscordBotConfig(settings)
db_config = DatabaseConfig(settings)


def get_settings() -> Settings:
    """獲取設定實例"""
    return settings


def validate_settings():
    """驗證設定完整性"""
    required_fields = [
        "discord_bot_token",
        "mcp_server_api_key",
        "discord_bot_api_url",
        "webhook_secret",
        "jwt_secret_key"
    ]
    
    missing_fields = []
    for field in required_fields:
        if not getattr(settings, field, None):
            missing_fields.append(field.upper())
    
    if missing_fields:
        raise ValueError(
            f"缺少必要的環境變數: {', '.join(missing_fields)}\n"
            f"請檢查您的 .env 檔案或環境變數設定。"
        )


def setup_logging():
    """設置日誌配置"""
    import logging
    import structlog
    from pathlib import Path
    
    # 確保日誌目錄存在
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 設置日誌級別
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # 配置 structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # 配置標準 logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    return structlog.get_logger() 