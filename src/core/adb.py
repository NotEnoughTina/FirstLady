"""Core ADB functionality"""

import subprocess
from typing import List, Optional
from .logging import app_logger
import re
import time
import socket
import telnetlib
import os
import traceback

def get_device_list() -> List[str]:
    """Get list of connected devices"""
    try:
        # Try to run ADB directly first
        cmd = ["adb", "devices"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                shell=True  # Required for Windows compatibility
            )
        except FileNotFoundError:
            app_logger.error("ADB not found in PATH. Checking common Android SDK locations...")
            # Common SDK locations
            sdk_locations = [
                os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe"),
                "C:/Program Files/Android/platform-tools/adb.exe",
                os.path.expanduser("~/Android/Sdk/platform-tools/adb.exe")
            ]
            
            for adb_path in sdk_locations:
                if os.path.exists(adb_path):
                    app_logger.info(f"Found ADB at: {adb_path}")
                    cmd[0] = adb_path
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=True,
                        shell=True
                    )
                    break
            else:
                app_logger.error("ADB not found in common locations. Please ensure Android SDK platform-tools is installed")
                return []

        # Parse output and get device IDs
        lines = result.stdout.strip().split('\n')[1:]  # Skip first line
        devices = []
        for line in lines:
            if line.strip():
                device_id = line.split()[0]
                devices.append(device_id)
                app_logger.debug(f"Found device: {device_id}")
        
        return devices
            
    except Exception as e:
        app_logger.error(f"Error getting device list: {str(e)}")
        app_logger.debug(f"Full error details: {traceback.format_exc()}")
        return []

def launch_package(device_id: str, package_name: str):
    """Launch an app package"""
    subprocess.run(
        ['adb', '-s', device_id, 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def force_stop_package(device_id: str, package_name: str):
    """Force stop an app package"""
    subprocess.run(['adb', '-s', device_id, 'shell', 'am', 'force-stop', package_name])

def press_back(device_id: str) -> bool:
    """Press back button"""
    try:
        cmd = f"adb -s {device_id} shell input keyevent 4"
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        app_logger.error(f"Error pressing back: {e}")
        return False

def tap_screen(device_id: str, x: int, y: int) -> bool:
    """Tap screen at coordinates"""
    try:
        cmd = f"adb -s {device_id} shell input tap {x} {y}"
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        app_logger.error(f"Error tapping screen: {e}")
        return False

def swipe_screen(device_id: str, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 300) -> bool:
    """Swipe screen from start to end coordinates"""
    try:
        cmd = f"adb -s {device_id} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        app_logger.error(f"Error swiping screen: {e}")
        return False

def get_connected_device() -> Optional[str]:
    """Get the selected connected device ID"""
    devices = get_device_list()
    if not devices:
        app_logger.error("No devices connected")
        return None
    
    if len(devices) == 1:
        return devices[0]
    
    print("Multiple devices found. Please select one:")
    for i, device in enumerate(devices, start=1):
        print(f"{i}. {device}")
    
    while True:
        try:
            selection = int(input("Enter the number of the device: "))
            if 1 <= selection <= len(devices):
                return devices[selection - 1]
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_current_running_app(device_id):
    """
    Returns the package name of the currently running app on the device.
    """
    try:
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'dumpsys', 'window', 'windows'],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if 'mCurrentFocus' in line or 'mFocusedApp' in line:
                package_name = line.split('/')[0].split()[-1]
                app_logger.debug(f"Current running app: {package_name}")
                return package_name
        return None
    except subprocess.CalledProcessError as e:
        app_logger.exception(f"Failed to get current running app: {e}")
        return None

def long_press_screen(device_id: str, x: int, y: int, duration: int) -> bool:
    """Execute a long press at coordinates with specified duration
    
    Args:
        device_id: Device identifier
        x: X coordinate
        y: Y coordinate
        duration: Press duration in milliseconds
    """
    try:
        cmd = f'adb -s {device_id} shell input swipe {x} {y} {x} {y} {duration}'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        app_logger.error(f"Failed to execute long press on device {device_id}")
        return False

def get_screen_size(device_id: str) -> tuple[int, int]:
    """Get device screen size"""
    try:
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'wm', 'size'], 
            capture_output=True, 
            text=True
        )
        match = re.search(r'(\d+)x(\d+)', result.stdout)
        if match:
            return int(match.group(1)), int(match.group(2))
        raise ValueError("Could not parse screen size")
    except Exception as e:
        raise RuntimeError(f"Failed to get screen size: {e}")
    
def simulate_shake(device_id: str, duration_ms: int = 1000) -> bool:
    """Simulate device shake using appropriate method for emulator or real device
    
    Args:
        device_id: The device identifier
        duration_ms: Duration of shake in milliseconds (default 1000ms)
    
    Returns:
        bool: True if shake simulation succeeded, False otherwise
    """
    try:
        # Check if device is an emulator
        app_logger.debug("Using emulator shake simulation")
        
        # Different shake patterns
        shake_patterns = [
            # Strong side shake
            ("100:0:9.81", "-100:0:9.81"),
            # Strong up/down shake
            ("0:100:9.81", "0:-100:9.81"),
            # Diagonal shake
            ("100:100:9.81", "-100:-100:9.81"),
            # Very strong shake
            ("200:200:9.81", "-200:-200:9.81"),
        ]
        
        for pattern in shake_patterns:
            app_logger.info(f"Trying shake pattern: {pattern}")
            
            for values in pattern:
                # Use the full adb shell command instead of emu
                cmd = f'adb -s {device_id} shell "setprop debug.sensors.accelerometer.x {values.split(":")[0]};' \
                      f'setprop debug.sensors.accelerometer.y {values.split(":")[1]};' \
                      f'setprop debug.sensors.accelerometer.z {values.split(":")[2]}"'
                app_logger.debug(f"Executing: {cmd}")
                subprocess.run(cmd, shell=True)
                time.sleep(0.1)
                
            # Reset to normal
            cmd = f'adb -s {device_id} shell "setprop debug.sensors.accelerometer.x 0;' \
                  f'setprop debug.sensors.accelerometer.y 0;' \
                  f'setprop debug.sensors.accelerometer.z 9.81"'
            subprocess.run(cmd, shell=True)
            time.sleep(0.2)
            
        return True
            
    except Exception as e:
        app_logger.error(f"Error simulating shake: {e}")
        return False
