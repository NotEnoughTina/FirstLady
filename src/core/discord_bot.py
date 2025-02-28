from discord import Webhook, Embed, File
from dotenv import load_dotenv
import os
import aiohttp
from src.core.logging import app_logger, log_exception

load_dotenv()

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
    async def send_notification(self, content: str = None, embeds: list = None, username: str = "Game Bot", file_path: str = None) -> bool:
        """Send notification to Discord webhook"""
        try:
            if not self.webhook_url:
                app_logger.error("Discord webhook URL not configured")
                return False
                
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(self.webhook_url, session=session)
                
                # Handle file upload if path provided
                file = None
                if file_path and os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            file = File(f)
                    except Exception as e:
                        log_exception(e, f"Failed to open file {file_path}")
                        return False
                
                # Ensure embeds is either a list or None, not False
                if embeds is not None and not isinstance(embeds, list):
                    embeds = [embeds] if embeds else None
                
                try:
                    await webhook.send(
                        content=content,
                        embeds=embeds,  # Now properly handled
                        username=username,
                        file=file
                    )
                    return True
                except Exception as e:
                    log_exception(e, "Failed to send webhook message")
                    return False
                    
        except Exception as e:
            log_exception(e, "Failed to initialize Discord notification")
            return False