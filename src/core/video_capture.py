import os
import time
from datetime import datetime
import logging
import subprocess
from threading import Thread, Event
from src.core.logging import app_logger
import shutil

logger = logging.getLogger(__name__)

class VideoCapture:
    def __init__(self, output_dir="records", max_folder_size_gb=2):
        """Initialize the video capture system.
        
        Args:
            output_dir (str): Directory where recordings will be stored
            max_folder_size_gb (int): Maximum size of the output directory in GB
        """
        self.output_dir = output_dir
        self.max_folder_size_gb = max_folder_size_gb
        self.recording = False
        self._stop_event = Event()
        self._recording_thread = None
        self.current_video = None
        self.device_id = None
        self.adb_process = None
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def set_device(self, device_id: str):
        """Set the device ID for ADB recording"""
        self.device_id = device_id
        
    def cleanup_device_recording(self):
        """Clean up temporary recording file from device"""
        if self.device_id:
            try:
                subprocess.run(
                    ["adb", "-s", self.device_id, "shell", "rm", "-f", "/sdcard/recording_temp.mp4"],
                    capture_output=True,
                    text=True
                )
            except Exception as e:
                app_logger.error(f"Error cleaning up device recording: {e}")
                
    def rotate_old_recordings(self):
        """Delete oldest recordings if folder size exceeds limit"""
        try:
            # Get total size of records folder in bytes
            total_size = sum(
                os.path.getsize(os.path.join(self.output_dir, f))
                for f in os.listdir(self.output_dir)
                if os.path.isfile(os.path.join(self.output_dir, f))
            )
            
            # Convert GB limit to bytes
            max_size_bytes = self.max_folder_size_gb * 1024 * 1024 * 1024
            
            if total_size > max_size_bytes:
                # Get list of files with their timestamps
                files = [
                    (f, os.path.getmtime(os.path.join(self.output_dir, f)))
                    for f in os.listdir(self.output_dir)
                    if os.path.isfile(os.path.join(self.output_dir, f))
                ]
                
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x[1])
                
                # Delete oldest files until under size limit
                for file_name, _ in files:
                    if total_size <= max_size_bytes:
                        break
                        
                    file_path = os.path.join(self.output_dir, file_name)
                    file_size = os.path.getsize(file_path)
                    try:
                        os.remove(file_path)
                        total_size -= file_size
                        app_logger.info(f"Rotated old recording: {file_name}")
                    except Exception as e:
                        app_logger.error(f"Error deleting old recording {file_name}: {e}")
                        
        except Exception as e:
            app_logger.error(f"Error rotating recordings: {e}")
            
    def start_recording(self, filename=None):
        """Start recording the device screen using ADB.
        
        Args:
            filename (str, optional): Custom filename for the recording.
                                    If None, generates timestamp-based filename.
        """
        if not self.device_id:
            logger.error("Device ID not set. Call set_device() first.")
            return
            
        if self.recording:
            logger.warning("Recording is already in progress")
            return
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.mp4"
            
        self.current_video = os.path.join(self.output_dir, filename)
        temp_device_path = "/sdcard/recording_temp.mp4"
        
        try:
            # Start recording on device
            adb_cmd = ["adb", "-s", self.device_id, "shell", "screenrecord", temp_device_path]
            self.adb_process = subprocess.Popen(adb_cmd)
            self.recording = True
            logger.info(f"Started ADB recording to {self.current_video}")
            
        except Exception as e:
            logger.error(f"Error starting ADB recording: {e}")
            self.recording = False
            if self.adb_process:
                self.adb_process.terminate()
                
    def stop_recording(self) -> bool:
        """Stop the current recording and pull it from the device"""
        if not self.recording or not self.adb_process:
            return False
            
        try:
            # Stop the recording process
            self.adb_process.terminate()
            self.adb_process.wait()
            self.adb_process = None
            self.recording = False
            
            # Wait a moment for the file to be written
            time.sleep(1)
            
            # Pull recording from device
            result = subprocess.run(
                ["adb", "-s", self.device_id, "pull", "/sdcard/recording_temp.mp4", self.current_video],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                app_logger.error(f"Failed to pull recording: {result.stderr}")
                return False
                
            # Clean up temp file and rotate old recordings
            self.cleanup_device_recording()
            self.rotate_old_recordings()
            
            return True
            
        except Exception as e:
            app_logger.error(f"Error stopping recording: {e}")
            return False 