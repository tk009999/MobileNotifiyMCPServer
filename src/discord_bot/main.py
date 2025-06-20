"""
Discord Bot 主程式
處理 Discord 互動和與 MCP Server 的通信
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
import discord
from discord.ext import commands, tasks
import httpx
import structlog

from ..shared.config import settings, setup_logging, validate_settings, discord_config
from ..shared.models import NotificationType, Priority

# 設置日誌
logger = setup_logging()

class NotificationBot(commands.Bot):
    """通知機器人類別"""
    
    def __init__(self):
        super().__init__(
            command_prefix=discord_config.command_prefix,
            intents=discord_config.bot_intents,
            help_command=None
        )
        
        self.logger = structlog.get_logger(__name__)
        self.http_client = httpx.AsyncClient()
        self.pending_responses = {}  # 儲存等待回覆的通知
    
    async def setup_hook(self):
        """設置機器人"""
        try:
            # 同步斜線命令
            await self.tree.sync()
            self.logger.info("斜線命令同步完成")
            
            # 啟動定期任務
            self.check_mcp_server.start()
            
        except Exception as e:
            self.logger.error(f"機器人設置失敗: {e}")
            raise
    
    async def on_ready(self):
        """機器人就緒事件"""
        self.logger.info(f"Discord Bot 已登入: {self.user} (ID: {self.user.id})")
        
        # 設置機器人狀態
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="工作進度 | /help"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """訊息事件處理"""
        # 忽略機器人自己的訊息
        if message.author == self.user:
            return
        
        # 檢查是否為回覆待處理的通知
        if message.reference and message.reference.message_id:
            await self.handle_notification_reply(message)
        
        # 處理命令
        await self.process_commands(message)
    
    async def handle_notification_reply(self, message):
        """處理通知回覆"""
        try:
            original_message_id = str(message.reference.message_id)
            
            if original_message_id in self.pending_responses:
                notification_id = self.pending_responses[original_message_id]
                
                # 發送回覆到 MCP Server
                await self.send_response_to_mcp(
                    notification_id=notification_id,
                    response_text=message.content,
                    user_id=str(message.author.id)
                )
                
                # 移除已處理的通知
                del self.pending_responses[original_message_id]
                
                # 回覆確認
                await message.add_reaction("✅")
                await message.reply("✅ 回覆已傳送給 AI 助手！", delete_after=5)
                
        except Exception as e:
            self.logger.error(f"處理通知回覆失敗: {e}")
            await message.add_reaction("❌")
    
    async def send_response_to_mcp(self, notification_id: str, response_text: str, user_id: str):
        """發送回覆到 MCP Server"""
        try:
            payload = {
                "notification_id": notification_id,
                "response_text": response_text,
                "user_id": user_id,
                "responded_at": datetime.utcnow().isoformat()
            }
            
            headers = {
                "Authorization": f"Bearer {settings.mcp_server_api_key}",
                "Content-Type": "application/json"
            }
            
            response = await self.http_client.post(
                f"http://{settings.mcp_server_host}:{settings.mcp_server_port}/api/v1/responses",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                self.logger.info(f"回覆發送成功: {notification_id}")
            else:
                self.logger.error(f"MCP Server 回應錯誤: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"發送回覆到 MCP Server 失敗: {e}")
    
    @tasks.loop(minutes=1)
    async def check_mcp_server(self):
        """定期檢查 MCP Server 狀態"""
        try:
            response = await self.http_client.get(
                f"http://{settings.mcp_server_host}:{settings.mcp_server_port}/health",
                timeout=10.0
            )
            
            if response.status_code != 200:
                self.logger.warning("MCP Server 健康檢查失敗")
                
        except Exception as e:
            self.logger.error(f"MCP Server 連接檢查失敗: {e}")
    
    async def close(self):
        """關閉機器人"""
        await self.http_client.aclose()
        await super().close()


# 建立機器人實例
bot = NotificationBot()


@bot.tree.command(name="status", description="查看系統狀態")
async def status_command(interaction: discord.Interaction):
    """查看系統狀態命令"""
    try:
        # 獲取 MCP Server 狀態
        response = await bot.http_client.get(
            f"http://{settings.mcp_server_host}:{settings.mcp_server_port}/health",
            timeout=10.0
        )
        
        if response.status_code == 200:
            health_data = response.json()
            
            embed = discord.Embed(
                title="🤖 系統狀態",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(
                name="MCP Server",
                value=f"✅ {health_data.get('mcp_server_status', 'unknown')}",
                inline=True
            )
            
            embed.add_field(
                name="資料庫",
                value=f"{'✅' if health_data.get('database_status') == 'healthy' else '❌'} {health_data.get('database_status', 'unknown')}",
                inline=True
            )
            
            embed.add_field(
                name="待處理通知",
                value=f"📬 {health_data.get('pending_notifications', 0)} 則",
                inline=True
            )
            
            embed.add_field(
                name="活躍專案",
                value=f"📊 {health_data.get('active_projects', 0)} 個",
                inline=True
            )
            
            embed.set_footer(text="DC 機器人推播通知器")
            
            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message("❌ 無法連接到 MCP Server", ephemeral=True)
            
    except Exception as e:
        bot.logger.error(f"狀態命令失敗: {e}")
        await interaction.response.send_message("❌ 獲取狀態失敗", ephemeral=True)


@bot.tree.command(name="help", description="顯示幫助資訊")
async def help_command(interaction: discord.Interaction):
    """幫助命令"""
    embed = discord.Embed(
        title="🤖 DC 機器人推播通知器",
        description="讓您透過 Discord 與 AI 助手無縫互動",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📱 基本功能",
        value=(
            "• 接收 AI 工作進度通知\n"
            "• 回覆 AI 的問題和詢問\n"
            "• 查看專案狀態\n"
            "• 管理通知設定"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 可用命令",
        value=(
            "`/status` - 查看系統狀態\n"
            "`/projects` - 列出活躍專案\n"
            "`/settings` - 通知設定\n"
            "`/help` - 顯示此幫助"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💬 如何回覆通知",
        value=(
            "當收到需要回覆的通知時，\n"
            "直接**回覆**該訊息即可！\n"
            "您的回覆會自動轉發給 AI 助手。"
        ),
        inline=False
    )
    
    embed.set_footer(text="MCP Server v1.0 | 有問題請聯繫開發者")
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="projects", description="列出活躍專案")
async def projects_command(interaction: discord.Interaction):
    """專案列表命令"""
    try:
        headers = {
            "Authorization": f"Bearer {settings.mcp_server_api_key}",
            "Content-Type": "application/json"
        }
        
        response = await bot.http_client.get(
            f"http://{settings.mcp_server_host}:{settings.mcp_server_port}/api/v1/projects",
            headers=headers,
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            projects = data.get("data", {}).get("projects", [])
            
            if not projects:
                await interaction.response.send_message("📋 目前沒有活躍的專案", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="📊 活躍專案",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            
            for project in projects[:10]:  # 最多顯示 10 個專案
                progress_bar = "▓" * (project.get("progress", 0) // 10) + "░" * (10 - (project.get("progress", 0) // 10))
                
                embed.add_field(
                    name=f"🎯 {project.get('name', 'Unknown')}",
                    value=(
                        f"**進度**: {project.get('progress', 0)}% {progress_bar}\n"
                        f"**目前任務**: {project.get('current_task', '無') or '無'}\n"
                        f"**狀態**: {project.get('status', '未知')}"
                    ),
                    inline=False
                )
            
            embed.set_footer(text=f"總共 {len(projects)} 個專案")
            
            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message("❌ 無法獲取專案列表", ephemeral=True)
            
    except Exception as e:
        bot.logger.error(f"專案命令失敗: {e}")
        await interaction.response.send_message("❌ 獲取專案失敗", ephemeral=True)


# Web API 端點（用於接收 MCP Server 的通知）
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer

api_app = FastAPI(title="Discord Bot API")
security = HTTPBearer()


def verify_webhook_secret(authorization: str = Header(None)):
    """驗證 Webhook 密鑰"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="無效的認證")
    
    token = authorization.replace("Bearer ", "")
    if token != settings.webhook_secret:
        raise HTTPException(status_code=401, detail="無效的 Webhook 密鑰")
    
    return token


@api_app.post("/api/notifications")
async def receive_notification(
    notification_data: Dict[str, Any],
    token: str = Depends(verify_webhook_secret)
):
    """接收來自 MCP Server 的通知"""
    try:
        notification_id = notification_data["notification_id"]
        notification_type = notification_data["type"]
        title = notification_data["title"]
        content = notification_data["content"]
        priority = notification_data["priority"]
        
        # 建立 Discord 嵌入訊息
        color_map = {
            "low": discord.Color.green(),
            "medium": discord.Color.orange(),
            "high": discord.Color.red(),
            "urgent": discord.Color.dark_red()
        }
        
        type_emoji = {
            "milestone": "🎯",
            "question": "❓",
            "alert": "⚠️",
            "status": "📊",
            "error": "❌"
        }
        
        embed = discord.Embed(
            title=f"{type_emoji.get(notification_type, '📢')} {title}",
            description=content,
            color=color_map.get(priority, discord.Color.blue()),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="優先級",
            value=f"{'🔴' if priority == 'urgent' else '🟡' if priority == 'high' else '🟢'} {priority.upper()}",
            inline=True
        )
        
        embed.set_footer(text=f"通知 ID: {notification_id[:8]}...")
        
        # 發送到用戶（這裡需要設定目標用戶 ID）
        # 暫時發送到第一個可用的頻道
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    message = await channel.send(embed=embed)
                    
                    # 如果是問題類型，記錄為待回覆
                    if notification_type == "question":
                        bot.pending_responses[str(message.id)] = notification_id
                        await message.add_reaction("💬")
                    
                    break
            break
        
        return {"success": True, "message": "通知發送成功"}
        
    except Exception as e:
        bot.logger.error(f"處理通知失敗: {e}")
        raise HTTPException(status_code=500, detail="處理通知失敗")


@api_app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "bot_ready": bot.is_ready(),
        "guilds": len(bot.guilds),
        "timestamp": datetime.utcnow().isoformat()
    }


async def start_bot():
    """啟動機器人"""
    try:
        # 驗證設定
        validate_settings()
        
        # 啟動機器人
        await bot.start(settings.discord_bot_token)
        
    except Exception as e:
        logger.error(f"Discord Bot 啟動失敗: {e}")
        raise


if __name__ == "__main__":
    # 運行機器人
    asyncio.run(start_bot()) 