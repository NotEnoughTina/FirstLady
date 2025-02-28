from abc import ABC, abstractmethod
from datetime import datetime, timezone
import time
from src.core.logging import app_logger
from typing import Optional, Dict, Any

from src.game.controls import navigate_home

class RoutineBase(ABC):
    """Base class for all automation routines"""

    def __init__(self, device_id: str, automation=None) -> None:
        self.device_id = device_id
        self.automation = automation
        self.device = None if not automation else automation.device
        
    @abstractmethod
    def _execute(self) -> bool:
        """Execute the routine's main logic"""
        pass
    
    def start(self) -> bool:
        """Start the automation sequence with home navigation"""
        try:
            if not self.automation.game_state["is_home"]:
                if not navigate_home(self.device_id, True):
                    app_logger.error("Failed to navigate home after clearing dig")
                    return False
            self.automation.game_state["is_home"] = True
            return self._execute()
        except Exception as e:
            app_logger.error(f"Error in routine execution: {e}")
            return False
            
    def execute_with_error_handling(self, func, *args, **kwargs) -> bool:
        """Execute a function with standard error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app_logger.error(f"Error in {func.__name__}: {e}")
            return False
    
    @abstractmethod
    def should_run(self) -> bool:
        """Check if the routine should run now"""
        pass
        
    @abstractmethod
    def after_run(self) -> None:
        """Actions to perform after successful run"""
        pass

class TimeCheckRoutine(RoutineBase):
    """Base class for time-based check routines"""
    
    def __init__(self, device_id: str, interval: int, last_run: float = None, automation=None) -> None:
        super().__init__(device_id, automation)
        self.interval = interval
        self._last_run = last_run or 0
        self.automation = automation
        
    def should_run(self) -> bool:
        if self._last_run is None:
            return True
        return time.time() - self._last_run >= self.interval
        
    def after_run(self) -> None:
        self._last_run = time.time()

class ScheduledRoutine(RoutineBase):
    """Base class for daily scheduled routines"""
    
    def __init__(self, device_id: str, automation=None, **kwargs):
        super().__init__(device_id, automation)
        # Extract schedule from kwargs
        self.schedule = kwargs.get('schedule', {})
        self.last_check = kwargs.get('last_check', None)
        
    def should_run(self) -> bool:
        """Determine if routine should run based on schedule or immediate mode"""
        if not self.schedule:
            # No schedule means run immediately
            return True
            
        current_dt = datetime.now(timezone.utc)
        
        # Check if already run today
        if self.last_check and datetime.fromtimestamp(self.last_check, timezone.utc).date() == current_dt.date():
            return False
            
        # Check schedule
        if self.schedule.get("day"):
            if current_dt.strftime('%A').lower() != self.schedule["day"].lower():
                return False
                
        if self.schedule.get("time"):
            target_hour, target_min = map(int, self.schedule["time"].split(':'))
            target_dt = current_dt.replace(hour=target_hour, minute=target_min)
            time_diff = abs((current_dt - target_dt).total_seconds() / 60)
            
            # Run if within 5 minute window of target time
            return time_diff <= 5
            
        return True
    
    def after_run(self) -> None:
        self.last_run = time.time() 