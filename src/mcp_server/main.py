"""
MCP Server 主程式
處理與 Cursor/Claude 的 MCP 協議通信
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import structlog
import httpx

from ..shared.config import settings, setup_logging, validate_settings
from ..shared.database import initialize_database, get_notification_repo, get_project_repo
from ..shared.models import (
    Notification, NotificationType, Priority, NotificationStatus,
    Project, WorkStatus, MCPResponse, SystemHealth
)

# 設置日誌
logger = setup_logging()

# FastAPI 應用程式
app = FastAPI(
    title="MCP Notification Server",
    description="DC 機器人推播通知器 MCP 服務器",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全設定
security = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """驗證 API 金鑰"""
    if credentials.credentials != settings.mcp_server_api_key:
        raise HTTPException(status_code=401, detail="無效的 API 金鑰")
    return credentials.credentials


class NotificationService:
    """通知服務"""
    
    def __init__(self):
        self.notification_repo = get_notification_repo()
        self.project_repo = get_project_repo()
        self.logger = structlog.get_logger(__name__)
        self.http_client = httpx.AsyncClient()
    
    async def send_notification_to_discord(self, notification: Notification) -> bool:
        """發送通知到 Discord Bot"""
        try:
            payload = {
                "notification_id": notification.id,
                "type": notification.type,
                "title": notification.title,
                "content": notification.content,
                "priority": notification.priority,
                "project_id": notification.project_id,
                "created_at": notification.created_at.isoformat()
            }
            
            headers = {
                "Authorization": f"Bearer {settings.webhook_secret}",
                "Content-Type": "application/json"
            }
            
            response = await self.http_client.post(
                f"{settings.discord_bot_api_url}/api/notifications",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                # 更新通知狀態為已發送
                self.notification_repo.update_notification_status(
                    notification.id, 
                    NotificationStatus.SENT,
                    "sent_at"
                )
                self.logger.info(f"通知發送成功: {notification.id}")
                return True
            else:
                self.logger.error(f"Discord Bot 回應錯誤: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"發送通知到 Discord 失敗: {e}")
            # 更新通知狀態為失敗
            self.notification_repo.update_notification_status(
                notification.id, 
                NotificationStatus.FAILED
            )
            return False
    
    async def process_pending_notifications(self):
        """處理待發送的通知"""
        try:
            pending_notifications = self.notification_repo.get_pending_notifications()
            
            for notification in pending_notifications:
                await self.send_notification_to_discord(notification)
                # 加入小延遲避免頻率限制
                await asyncio.sleep(1)
                
        except Exception as e:
            self.logger.error(f"處理待發送通知失敗: {e}")


# 通知服務實例
notification_service = NotificationService()


@app.on_event("startup")
async def startup_event():
    """應用程式啟動事件"""
    try:
        # 驗證設定
        validate_settings()
        
        # 初始化資料庫
        initialize_database()
        
        # 啟動背景任務處理通知
        asyncio.create_task(notification_processor())
        
        logger.info("MCP Server 啟動成功")
        
    except Exception as e:
        logger.error(f"MCP Server 啟動失敗: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉事件"""
    try:
        await notification_service.http_client.aclose()
        logger.info("MCP Server 關閉完成")
    except Exception as e:
        logger.error(f"MCP Server 關閉失敗: {e}")


async def notification_processor():
    """通知處理背景任務"""
    while True:
        try:
            await notification_service.process_pending_notifications()
            await asyncio.sleep(10)  # 每 10 秒檢查一次
        except Exception as e:
            logger.error(f"通知處理器錯誤: {e}")
            await asyncio.sleep(30)  # 發生錯誤時等待更長時間


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    try:
        # 檢查資料庫
        db_status = "healthy" if get_notification_repo().db_manager.health_check() else "unhealthy"
        
        # 檢查 Discord Bot 連接（簡單測試）
        discord_status = "unknown"
        try:
            response = await notification_service.http_client.get(
                f"{settings.discord_bot_api_url}/health",
                timeout=5.0
            )
            discord_status = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            discord_status = "unhealthy"
        
        return SystemHealth(
            mcp_server_status="healthy",
            discord_bot_status=discord_status,
            database_status=db_status,
            pending_notifications=len(get_notification_repo().get_pending_notifications()),
            active_projects=len(get_project_repo().get_active_projects())
        )
        
    except Exception as e:
        logger.error(f"健康檢查失敗: {e}")
        raise HTTPException(status_code=500, detail="健康檢查失敗")


@app.post("/api/v1/notifications")
async def create_notification(
    notification_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """建立通知"""
    try:
        # 驗證和建立通知物件
        notification = Notification(
            type=NotificationType(notification_data.get("type", "milestone")),
            title=notification_data["title"],
            content=notification_data["content"],
            priority=Priority(notification_data.get("priority", "medium")),
            project_id=notification_data.get("project_id"),
            metadata=notification_data.get("metadata", {})
        )
        
        # 儲存通知到資料庫
        notification_id = get_notification_repo().create_notification(notification)
        
        logger.info(f"通知建立成功: {notification_id}")
        
        return MCPResponse(
            success=True,
            data={
                "notification_id": notification_id,
                "message": "通知建立成功，正在處理發送"
            }
        )
        
    except Exception as e:
        logger.error(f"建立通知失敗: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


@app.get("/api/v1/notifications/{notification_id}")
async def get_notification(
    notification_id: str,
    api_key: str = Depends(verify_api_key)
):
    """獲取通知詳情"""
    try:
        notification = get_notification_repo().get_notification(notification_id)
        
        if not notification:
            raise HTTPException(status_code=404, detail="通知不存在")
        
        return MCPResponse(
            success=True,
            data=notification.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取通知失敗: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/v1/responses")
async def receive_response(
    response_data: Dict[str, Any],
    api_key: str = Depends(verify_api_key)
):
    """接收來自 Discord 的回覆"""
    try:
        notification_id = response_data["notification_id"]
        response_text = response_data["response_text"]
        user_id = response_data["user_id"]
        
        # 更新通知狀態為已回覆
        success = get_notification_repo().update_notification_status(
            notification_id, 
            NotificationStatus.REPLIED,
            "replied_at"
        )
        
        if success:
            logger.info(f"收到回覆: {notification_id} - {response_text[:50]}...")
            
            return MCPResponse(
                success=True,
                data={
                    "message": "回覆接收成功",
                    "notification_id": notification_id
                }
            )
        else:
            raise HTTPException(status_code=404, detail="通知不存在")
            
    except Exception as e:
        logger.error(f"接收回覆失敗: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


@app.put("/api/v1/work-status")
async def update_work_status(
    status_data: WorkStatus,
    api_key: str = Depends(verify_api_key)
):
    """更新工作狀態"""
    try:
        # 更新專案資訊
        project = get_project_repo().get_project(status_data.project_id)
        
        if project:
            project.current_task = status_data.current_task
            project.progress = status_data.progress
            project.estimated_completion = status_data.estimated_completion
            project.updated_at = datetime.utcnow()
            project.metadata.update(status_data.details)
            
            # 這裡應該有更新專案的方法，暫時省略實作
            logger.info(f"工作狀態更新: {status_data.project_id} - {status_data.progress}%")
        
        return MCPResponse(
            success=True,
            data={"message": "工作狀態更新成功"}
        )
        
    except Exception as e:
        logger.error(f"更新工作狀態失敗: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


@app.get("/api/v1/projects")
async def list_projects(api_key: str = Depends(verify_api_key)):
    """列出活躍專案"""
    try:
        projects = get_project_repo().get_active_projects()
        
        return MCPResponse(
            success=True,
            data={
                "projects": [project.dict() for project in projects],
                "count": len(projects)
            }
        )
        
    except Exception as e:
        logger.error(f"獲取專案列表失敗: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    uvicorn.run(
        "src.mcp_server.main:app",
        host=settings.mcp_server_host,
        port=settings.mcp_server_port,
        reload=True,
        log_level=settings.log_level.lower()
    ) 