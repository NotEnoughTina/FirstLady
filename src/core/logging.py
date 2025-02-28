"""Logging configuration"""

import logging
import sys
from pathlib import Path
import traceback

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

class ErrorLogFormatter(logging.Formatter):
    """Custom formatter that includes traceback for errors"""
    def format(self, record):
        if record.levelno >= logging.ERROR and hasattr(record, 'stack_info'):
            if record.exc_info:
                record.error_details = ''.join(traceback.format_exception(*record.exc_info))
            elif record.stack_info:
                record.error_details = record.stack_info
            else:
                record.error_details = 'No stack trace available'
        return super().format(record)

# Configure main file handler
file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Configure error file handler with custom formatter
error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(ErrorLogFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
    'Error Details:\n%(error_details)s\n'
))

# Configure console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
))

# Setup app logger
app_logger = logging.getLogger('app')
app_logger.addHandler(file_handler)
app_logger.addHandler(error_handler)
app_logger.addHandler(console_handler)

def log_exception(e: Exception, message: str = None):
    """Log exception with full traceback"""
    error_msg = f"{message + ': ' if message else ''}{str(e)}"
    app_logger.error(error_msg, exc_info=True, stack_info=True)

def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    app_logger.setLevel(level)

def log_error(logger, message: str, exc: Exception = None):
    """Helper function to log errors with file and line information"""
    if exc:
        tb = traceback.extract_tb(exc.__traceback__)
        filename, line_no, func, _ = tb[-1]  # Get the last frame
        logger.error(f"{message} at {filename}:{line_no} in {func}: {str(exc)}")
    else:
        frame = traceback.extract_stack()[-2]  # Get caller's frame
        filename, line_no, func, _ = frame
        logger.error(f"{message} at {filename}:{line_no} in {func}")