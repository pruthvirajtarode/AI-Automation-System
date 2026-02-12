"""
Logging and Monitoring Utilities
"""

import logging
from datetime import datetime

class LogFormatter(logging.Formatter):
    """Custom log formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[41m',   # Red background
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        """Format log message with colors"""
        if record.levelname in self.COLORS:
            record.levelname = (
                self.COLORS[record.levelname] + 
                record.levelname + 
                self.COLORS['RESET']
            )
        return super().format(record)

def setup_logging(app_name: str, log_level: int = logging.INFO):
    """Setup application logging"""
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    formatter = LogFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger
