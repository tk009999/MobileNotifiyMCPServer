"""
共用資料模型
定義系統中使用的各種資料結構
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    """通知類型枚舉"""
    MILESTONE = "milestone"      # 里程碑通知
    QUESTION = "question"        # 問題詢問
    ALERT = "alert"             # 警報通知
    STATUS = "status"           # 狀態更新
    ERROR = "error"             # 錯誤通知


class Priority(str, Enum):
    """優先級枚舉"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationStatus(str, Enum):
    """通知狀態枚舉"""
    PENDING = "pending"         # 待發送
    SENT = "sent"              # 已發送
    DELIVERED = "delivered"     # 已送達
    READ = "read"              # 已讀取
    REPLIED = "replied"        # 已回覆
    FAILED = "failed"          # 發送失敗


class ProjectStatus(str, Enum):
    """專案狀態枚舉"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Notification(BaseModel):
    """通知資料模型"""
    id: Optional[str] = None
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    priority: Priority = Priority.MEDIUM
    project_id: Optional[str] = None
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class NotificationResponse(BaseModel):
    """通知回覆資料模型"""
    notification_id: str
    response_text: str = Field(..., min_length=1, max_length=1000)
    user_id: str
    responded_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Project(BaseModel):
    """專案資料模型"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    current_task: Optional[str] = None
    progress: int = Field(default=0, ge=0, le=100)
    estimated_completion: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class WorkStatus(BaseModel):
    """工作狀態資料模型"""
    project_id: str
    current_task: str = Field(..., min_length=1, max_length=200)
    progress: int = Field(..., ge=0, le=100)
    estimated_completion: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    details: Dict[str, Any] = Field(default_factory=dict)


class UserPreferences(BaseModel):
    """使用者偏好設定資料模型"""
    user_id: str
    notification_types: List[NotificationType] = Field(
        default_factory=lambda: [NotificationType.MILESTONE, NotificationType.QUESTION]
    )
    quiet_hours_start: str = "22:00"
    quiet_hours_end: str = "08:00"
    priority_filter: Priority = Priority.LOW
    discord_dm: bool = True
    discord_channel_id: Optional[str] = None
    timezone: str = "UTC"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class MCPRequest(BaseModel):
    """MCP 請求資料模型"""
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MCPResponse(BaseModel):
    """MCP 回應資料模型"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DiscordMessage(BaseModel):
    """Discord 訊息資料模型"""
    user_id: str
    channel_id: str
    message_id: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_reply: bool = False
    reply_to_notification_id: Optional[str] = None


class SystemHealth(BaseModel):
    """系統健康狀態資料模型"""
    mcp_server_status: str = "unknown"
    discord_bot_status: str = "unknown"
    database_status: str = "unknown"
    last_notification_sent: Optional[datetime] = None
    active_projects: int = 0
    pending_notifications: int = 0
    system_uptime: Optional[float] = None
    last_check: datetime = Field(default_factory=datetime.utcnow) 