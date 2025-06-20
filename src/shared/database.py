"""
資料庫操作模組
處理資料庫連接、表格定義和基本操作
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import structlog

from .config import settings, db_config
from .models import (
    NotificationType, Priority, NotificationStatus, ProjectStatus,
    Notification, Project, NotificationResponse, UserPreferences
)

logger = structlog.get_logger(__name__)

# 資料庫基礎類別
Base = declarative_base()


class NotificationTable(Base):
    """通知資料表"""
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    project_id = Column(String, nullable=True)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, default=dict)


class ProjectTable(Base):
    """專案資料表"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    current_task = Column(String(200), nullable=True)
    progress = Column(Integer, default=0)
    estimated_completion = Column(DateTime, nullable=True)
    metadata = Column(JSON, default=dict)


class NotificationResponseTable(Base):
    """通知回覆資料表"""
    __tablename__ = "notification_responses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id = Column(String, nullable=False)
    response_text = Column(String(1000), nullable=False)
    user_id = Column(String, nullable=False)
    responded_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)


class UserPreferencesTable(Base):
    """使用者偏好設定資料表"""
    __tablename__ = "user_preferences"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True, nullable=False)
    notification_types = Column(JSON, default=["milestone", "question"])
    quiet_hours_start = Column(String(5), default="22:00")
    quiet_hours_end = Column(String(5), default="08:00")
    priority_filter = Column(Enum(Priority), default=Priority.LOW)
    discord_dm = Column(Boolean, default=True)
    discord_channel_id = Column(String, nullable=True)
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseManager:
    """資料庫管理器"""
    
    def __init__(self):
        self.engine = create_engine(settings.database_url, **db_config.engine_kwargs)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = structlog.get_logger(__name__)
    
    def create_tables(self):
        """建立資料表"""
        try:
            Base.metadata.create_all(bind=self.engine)
            self.logger.info("資料表建立成功")
        except Exception as e:
            self.logger.error(f"資料表建立失敗: {e}")
            raise
    
    def get_session(self) -> Session:
        """獲取資料庫會話"""
        return self.SessionLocal()
    
    def health_check(self) -> bool:
        """資料庫健康檢查"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"資料庫健康檢查失敗: {e}")
            return False


class NotificationRepository:
    """通知資料存取物件"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = structlog.get_logger(__name__)
    
    def create_notification(self, notification: Notification) -> str:
        """建立通知"""
        try:
            with self.db_manager.get_session() as session:
                db_notification = NotificationTable(
                    type=notification.type,
                    title=notification.title,
                    content=notification.content,
                    priority=notification.priority,
                    project_id=notification.project_id,
                    metadata=notification.metadata
                )
                session.add(db_notification)
                session.commit()
                session.refresh(db_notification)
                
                self.logger.info(f"通知建立成功: {db_notification.id}")
                return db_notification.id
        except Exception as e:
            self.logger.error(f"建立通知失敗: {e}")
            raise
    
    def get_notification(self, notification_id: str) -> Optional[Notification]:
        """獲取通知"""
        try:
            with self.db_manager.get_session() as session:
                db_notification = session.query(NotificationTable).filter(
                    NotificationTable.id == notification_id
                ).first()
                
                if db_notification:
                    return Notification(
                        id=db_notification.id,
                        type=db_notification.type,
                        title=db_notification.title,
                        content=db_notification.content,
                        priority=db_notification.priority,
                        project_id=db_notification.project_id,
                        status=db_notification.status,
                        created_at=db_notification.created_at,
                        sent_at=db_notification.sent_at,
                        read_at=db_notification.read_at,
                        replied_at=db_notification.replied_at,
                        metadata=db_notification.metadata
                    )
                return None
        except Exception as e:
            self.logger.error(f"獲取通知失敗: {e}")
            return None
    
    def update_notification_status(self, notification_id: str, status: NotificationStatus, 
                                 timestamp_field: Optional[str] = None) -> bool:
        """更新通知狀態"""
        try:
            with self.db_manager.get_session() as session:
                db_notification = session.query(NotificationTable).filter(
                    NotificationTable.id == notification_id
                ).first()
                
                if db_notification:
                    db_notification.status = status
                    
                    if timestamp_field:
                        setattr(db_notification, timestamp_field, datetime.utcnow())
                    
                    session.commit()
                    self.logger.info(f"通知狀態更新成功: {notification_id} -> {status}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"更新通知狀態失敗: {e}")
            return False
    
    def get_pending_notifications(self) -> List[Notification]:
        """獲取待發送的通知"""
        try:
            with self.db_manager.get_session() as session:
                db_notifications = session.query(NotificationTable).filter(
                    NotificationTable.status == NotificationStatus.PENDING
                ).order_by(NotificationTable.created_at.asc()).all()
                
                notifications = []
                for db_notification in db_notifications:
                    notifications.append(Notification(
                        id=db_notification.id,
                        type=db_notification.type,
                        title=db_notification.title,
                        content=db_notification.content,
                        priority=db_notification.priority,
                        project_id=db_notification.project_id,
                        status=db_notification.status,
                        created_at=db_notification.created_at,
                        sent_at=db_notification.sent_at,
                        read_at=db_notification.read_at,
                        replied_at=db_notification.replied_at,
                        metadata=db_notification.metadata
                    ))
                
                return notifications
        except Exception as e:
            self.logger.error(f"獲取待發送通知失敗: {e}")
            return []


class ProjectRepository:
    """專案資料存取物件"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = structlog.get_logger(__name__)
    
    def create_project(self, project: Project) -> str:
        """建立專案"""
        try:
            with self.db_manager.get_session() as session:
                db_project = ProjectTable(
                    name=project.name,
                    description=project.description,
                    status=project.status,
                    current_task=project.current_task,
                    progress=project.progress,
                    estimated_completion=project.estimated_completion,
                    metadata=project.metadata
                )
                session.add(db_project)
                session.commit()
                session.refresh(db_project)
                
                self.logger.info(f"專案建立成功: {db_project.id}")
                return db_project.id
        except Exception as e:
            self.logger.error(f"建立專案失敗: {e}")
            raise
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """獲取專案"""
        try:
            with self.db_manager.get_session() as session:
                db_project = session.query(ProjectTable).filter(
                    ProjectTable.id == project_id
                ).first()
                
                if db_project:
                    return Project(
                        id=db_project.id,
                        name=db_project.name,
                        description=db_project.description,
                        status=db_project.status,
                        created_at=db_project.created_at,
                        updated_at=db_project.updated_at,
                        current_task=db_project.current_task,
                        progress=db_project.progress,
                        estimated_completion=db_project.estimated_completion,
                        metadata=db_project.metadata
                    )
                return None
        except Exception as e:
            self.logger.error(f"獲取專案失敗: {e}")
            return None
    
    def get_active_projects(self) -> List[Project]:
        """獲取活躍專案"""
        try:
            with self.db_manager.get_session() as session:
                db_projects = session.query(ProjectTable).filter(
                    ProjectTable.status == ProjectStatus.ACTIVE
                ).order_by(ProjectTable.updated_at.desc()).all()
                
                projects = []
                for db_project in db_projects:
                    projects.append(Project(
                        id=db_project.id,
                        name=db_project.name,
                        description=db_project.description,
                        status=db_project.status,
                        created_at=db_project.created_at,
                        updated_at=db_project.updated_at,
                        current_task=db_project.current_task,
                        progress=db_project.progress,
                        estimated_completion=db_project.estimated_completion,
                        metadata=db_project.metadata
                    ))
                
                return projects
        except Exception as e:
            self.logger.error(f"獲取活躍專案失敗: {e}")
            return []


# 全域資料庫管理器實例
db_manager = DatabaseManager()
notification_repo = NotificationRepository(db_manager)
project_repo = ProjectRepository(db_manager)


def initialize_database():
    """初始化資料庫"""
    try:
        db_manager.create_tables()
        logger.info("資料庫初始化完成")
    except Exception as e:
        logger.error(f"資料庫初始化失敗: {e}")
        raise


def get_db_manager() -> DatabaseManager:
    """獲取資料庫管理器"""
    return db_manager


def get_notification_repo() -> NotificationRepository:
    """獲取通知資料存取物件"""
    return notification_repo


def get_project_repo() -> ProjectRepository:
    """獲取專案資料存取物件"""
    return project_repo 