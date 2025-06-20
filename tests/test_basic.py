"""
基本功能測試
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.shared.models import Notification, NotificationType, Priority
from src.shared.config import Settings


class TestNotificationModel:
    """通知模型測試"""
    
    def test_notification_creation(self):
        """測試通知建立"""
        notification = Notification(
            type=NotificationType.MILESTONE,
            title="測試通知",
            content="這是一個測試通知",
            priority=Priority.HIGH
        )
        
        assert notification.type == NotificationType.MILESTONE
        assert notification.title == "測試通知"
        assert notification.content == "這是一個測試通知"
        assert notification.priority == Priority.HIGH
    
    def test_notification_validation(self):
        """測試通知驗證"""
        with pytest.raises(ValueError):
            Notification(
                type=NotificationType.MILESTONE,
                title="",  # 空標題應該失敗
                content="測試內容"
            )


class TestSettings:
    """設定測試"""
    
    @patch.dict('os.environ', {
        'DISCORD_BOT_TOKEN': 'test_token',
        'MCP_SERVER_API_KEY': 'test_api_key',
        'DISCORD_BOT_API_URL': 'https://test.com',
        'WEBHOOK_SECRET': 'test_secret',
        'JWT_SECRET_KEY': 'test_jwt_secret'
    })
    def test_settings_validation(self):
        """測試設定驗證"""
        from src.shared.config import validate_settings
        
        # 應該不會拋出異常
        validate_settings()
    
    def test_cors_origins_parsing(self):
        """測試 CORS 來源解析"""
        settings = Settings()
        
        # 測試預設值
        origins = settings.get_cors_origins()
        assert isinstance(origins, list)


if __name__ == "__main__":
    pytest.main([__file__]) 