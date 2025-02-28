from src.automation.routines import ScheduledRoutine
from src.core.adb import get_screen_size
from src.core.config import CONFIG
from src.core.image_processing import find_and_tap_template
from src.core.video_capture import VideoCapture
from src.core.logging import app_logger
from datetime import datetime, timezone
import time
import os
import asyncio
from discord import File
from src.core.discord_bot import DiscordNotifier

from src.game.controls import handle_swipes, human_delay, humanized_tap

class WeeklyVsCaptureRoutine(ScheduledRoutine):
    """Routine for recording game screen via ADB at scheduled times or immediately"""
    
    def __init__(self, device_id: str, automation=None, **kwargs):
        super().__init__(device_id, automation=automation, **kwargs)
        self.video_capture = VideoCapture()
        self.video_capture.set_device(device_id)

    def _execute(self) -> bool:
        """Execute the video recording routine"""
        try:
            if not self.navigate_to_weekly_vs():
                return False
            
            # Generate a filename with the date
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weekly_vs_recording_{timestamp}.mp4"

            # Start recording
            app_logger.info(f"Starting ADB video recording: {filename}")
            self.video_capture.start_recording(filename)
            
            # Get screen dimensions for swipe
            width, height = get_screen_size(self.device_id)
            start_x = int(width * 0.5)  # 50% of screen width
            start_y = int(height * 0.60)  # 75% of screen height
            end_y = int(height * 0.3)  # 30% of screen height
            
            # Perform custom swipes
            for i in range(19):
                self.device.shell(
                    f'input swipe {start_x} {start_y} {start_x} {end_y} 500'
                )  # 500ms duration for slow swipe
                human_delay(1)

            # Stop recording
            self.video_capture.stop_recording()
            app_logger.info("Weekly video recording completed")
            
            # Send to Discord webhook if configured
            video_path = os.path.join(self.video_capture.output_dir, filename)
            asyncio.run(self.send_to_discord(video_path))
            
            return True
            
        except Exception as e:
            from src.core.logging import log_exception
            log_exception(e, "Error in video recording routine")
            if self.video_capture.recording:
                self.video_capture.stop_recording()
            return False
        
    def after_run(self) -> None:
        """Update last check time after successful execution"""
        if self.automation:
            self.automation.state.set_last_run(
                "weekly_reset",
                time.time(),
                check_type="scheduled_events"
            )

    async def send_to_discord(self, video_path: str) -> bool:
        """Send video to Discord webhook"""
        try:
            webhook_url = os.getenv('VS_UPLOAD_WEBHOOK_URL')
            if not webhook_url:
                app_logger.error("VS_UPLOAD_WEBHOOK_URL not configured")
                return False
                
            discord = DiscordNotifier()
            discord.webhook_url = webhook_url
            
            if not os.path.exists(video_path):
                app_logger.error(f"Video file not found at {video_path}")
                return False
                
            await discord.send_notification(
                content="📊 **Weekly VS Rankings Recording**",
                file_path=video_path,
                username="VS Rankings Bot"
            )
            app_logger.info("Successfully sent video to Discord webhook")
            return True
            
        except Exception as e:
            from src.core.logging import log_exception
            log_exception(e, "Failed to send video to Discord")
            return False
        
    def navigate_to_weekly_vs(self) -> bool:
        """Navigate to the weekly vs page"""
        if not find_and_tap_template(
                self.device_id,
                "vs_menu",
                error_msg=f"Could not find vs button",
                critical=True
            ):
                return False
        
        if not find_and_tap_template(
                self.device_id,
                "points_ranking",
                error_msg=f"Could not find points_ranking button",
                critical=True
            ):
                return False
        
        if not find_and_tap_template(
                self.device_id,
                "weekly_rank",
                error_msg=f"Could not find weekly_rank button",
                critical=True
            ):
                return False
        
        self.alliance_toggle(self.device_id)
        
        return True

    def alliance_toggle(self, device_id: str) -> bool:
        """Open the profile menu"""
        try:
            width, height = get_screen_size(device_id)
            coords = CONFIG['ui_elements']['alliance_toggle']
            x = int(width * float(coords['x'].strip('%')) / 100)
            y = int(height * float(coords['y'].strip('%')) / 100)
            humanized_tap(device_id, x, y, True)
            return True
        except Exception as e:
            app_logger.error(f"Error opening profile menu: {e}")
            return False