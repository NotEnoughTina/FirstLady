"""Device interaction utilities"""

import subprocess
from typing import Tuple
from .logging import app_logger
from pathlib import Path
import shutil
from src.core.config import CONFIG

def take_screenshot(device_id: str) -> bool:
    """Take screenshot and pull to local tmp directory"""
    try:
        ensure_dir("tmp")

        # pipe = subprocess.Popen(f"{CONFIG.adb["binary_path"]} exec-out screencap -p",
        #                         stdin=subprocess.PIPE,
        #                         stdout=subprocess.PIPE, shell=True)
        # image_bytes = pipe.stdout.read()  # .replace(b'\r\n', b'\n')
        # image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        #
        # cv2.imwrite("tmp/screen.png", image)

        cmd = [CONFIG.adb["binary_path"], "exec-out", "screencap", "-p"]
        with open('tmp/screen.png', "w") as outfile:
            result = subprocess.run(cmd, stdout=outfile)
            if result.returncode != 0:
                app_logger.error(f"Failed to pull screenshot: {result.stderr}")
                return False

        # Clean up device screenshot
        cleanup_device_screenshots(device_id)
        return True
        
    except Exception as e:
        app_logger.error(f"Error taking screenshot: {e}")
        return False

def get_screen_size(device_id: str) -> Tuple[int, int]:
    """Get screen size from device"""
    try:
        cmd = f"{CONFIG.adb['binary_path']} -s {device_id} shell wm size"
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            app_logger.error(f"Failed to get screen size: {result.stderr}")
            return (1920, 1080)  # Default fallback
            
        # Parse output like "Physical size: 1920x1080"
        size = result.stdout.strip().split(": ")[1].split("x")
        return (int(size[0]), int(size[1]))
        
    except Exception as e:
        app_logger.error(f"Error getting screen size: {e}")
        return (1920, 1080)  # Default fallback

def cleanup_device_screenshots(device_id: str) -> None:
    """Clean up screenshots from device"""
    try:
        cmd = f"{CONFIG.adb['binary_path']} -s {device_id} shell rm -f /sdcard/screen*.png"
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            app_logger.debug("Cleaned up device screenshots")
        else:
            app_logger.warning(f"Failed to clean device screenshots: {result.stderr}")
    except Exception as e:
        app_logger.error(f"Error cleaning device screenshots: {e}")

def cleanup_temp_files() -> None:
    """Clean up temporary files"""
    try:
        # Remove entire tmp directory and its contents recursively
        tmp_dir = Path("tmp")
        if tmp_dir.exists():
            for item in tmp_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        app_logger.debug(f"Cleaned up temporary file: {item}")
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                        app_logger.debug(f"Cleaned up temporary directory: {item}")
                except Exception as e:
                    app_logger.warning(f"Failed to delete {item}: {e}")
            
            try:
                tmp_dir.rmdir()
                app_logger.debug("Cleaned up main temporary directory")
            except Exception as e:
                app_logger.warning(f"Failed to delete tmp directory: {e}")
    except Exception as e:
        app_logger.error(f"Error cleaning temporary files: {e}")

def cleanup(device_id: str) -> None:
    """Cleanup device and local temp files"""
    cleanup_device_screenshots(device_id)
    cleanup_temp_files()

def ensure_dir(path: str) -> None:
    """Ensure directory exists"""
    Path(path).mkdir(exist_ok=True)