#!/usr/bin/env python3

import sys
import argparse
import traceback
import time
import json
from pathlib import Path
import signal
from src.core.logging import setup_logging, app_logger
from src.core.device import cleanup_temp_files, cleanup_device_screenshots, ensure_dir
from src.core.adb import get_connected_device
from src.automation.automation import MainAutomation
from src.core.cleanup import CleanupManager
from src.automation.handler_factory import HandlerFactory

def get_routine_config():
    try:
        with open("config/automation.json") as f:
            config = json.load(f)
            # Get both time checks and scheduled events
            routines = {}
            
            # Add time checks
            time_checks = {
                name: data 
                for name, data in config.get("time_checks", {}).items()
                if data.get("interval") is not None
            }
            routines.update(time_checks)
            
            # Add scheduled events
            scheduled_events = config.get("scheduled_events", {})
            routines.update(scheduled_events)
            
            return routines
    except Exception:
        return {}

parser = argparse.ArgumentParser(description='Game automation CLI')
parser.add_argument('command', choices=['auto', 'routine', 'reset'], help='Automation command to run')
parser.add_argument('routine_name', nargs='?', choices=list(get_routine_config().keys()), help='Name of routine to run')
parser.add_argument('--debug', action='store_true', help='Enable debug logging')
parser.add_argument('--no-cleanup', action='store_true', help='Skip cleanup on exit')

cleanup_manager = CleanupManager()

def cleanup():
    """Cleanup resources"""
    cleanup_manager.cleanup()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    app_logger.info("\nShutdown requested, cleaning up...")
    cleanup()
    sys.exit(0)

def run_single_routine(device_id: str, routine_name: str) -> bool:
    """Run a single routine"""
    try:
        with open("config/automation.json") as f:
            config = json.load(f)
            
        # Check in both time_checks and scheduled_events
        routine_config = config.get("time_checks", {}).get(routine_name) or config.get("scheduled_events", {}).get(routine_name)
        
        if not routine_config:
            app_logger.error(f"Routine {routine_name} not found in config")
            return False
            
        # Create automation instance
        automation = MainAutomation(device_id, debug=True)
        
        handler_factory = HandlerFactory()
        handler_args = {
            "interval": routine_config.get("interval"),
            "schedule": routine_config.get("schedule")
        }
        
        handler = handler_factory.create_handler(
            routine_config["handler"],
            device_id,
            handler_args,
            automation=automation
        )
        
        if handler:
            app_logger.info(f"Running {routine_name} routine")
            return handler.start()
        return False
        
    except Exception as e:
        app_logger.error(f"Error running routine {routine_name}: {e}")
        return False

def main():
    args = parser.parse_args()
    setup_logging()
    
    device_id = get_connected_device()
    if not device_id:
        app_logger.error("No devices found. Please check:")
        app_logger.error("1. Device is connected via USB")
        app_logger.error("2. USB debugging is enabled")
        app_logger.error("3. Computer is authorized for USB debugging")
        sys.exit(1)
    
    app_logger.info(f"Connected to device: {device_id}")
    
    cleanup_manager.set_device(device_id)
    cleanup_manager.set_skip_cleanup(args.no_cleanup)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if args.command == 'routine':
            if not args.routine_name:
                app_logger.error("No routine specified")
                return 1
            success = run_single_routine(device_id, args.routine_name)
            return 0 if success else 1
            
        elif args.command == 'auto':
            automation = MainAutomation(device_id, debug=args.debug)
            success = automation.run()
            return 0 if success else 1
            
        elif args.command == 'reset':
            automation = MainAutomation(device_id, debug=args.debug)
            success = automation.force_reset()
            if not success:
                app_logger.error("Failed to reset game")
                sys.exit(1)
            
    except Exception as e:
        app_logger.error(f"Error in main: {e}")
        if args.debug:
            traceback.print_exc()
        return 1
    finally:
        cleanup()

if __name__ == '__main__':
    sys.exit(main()) 