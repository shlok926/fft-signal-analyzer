"""
Production-Grade Logger - File + Console + Error Tracking
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import sys
import traceback

class ProductionLogger:
    """Professional logging system with file rotation and error tracking"""
    
    _instance = None
    _loggers = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Create rotating file handler (with UTF-8 encoding)
        log_file = self.log_dir / f"fft_analyzer_{datetime.now().strftime('%Y%m%d')}.log"
        
        self.file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # Console handler
        self.console_handler = logging.StreamHandler(sys.stdout)
        
        # Formatter
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)
    
    def get_logger(self, name):
        """Get or create a logger"""
        if name not in self._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            
            # Add handlers if not already present
            if not logger.handlers:
                logger.addHandler(self.file_handler)
                logger.addHandler(self.console_handler)
            
            self._loggers[name] = logger
        
        return self._loggers[name]
    
    @staticmethod
    def log_exception(logger, exception, context=""):
        """Log exception with full traceback"""
        error_msg = f"Exception in {context}: {str(exception)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return error_msg
    
    @staticmethod
    def log_performance(logger, operation_name, duration_ms):
        """Log operation performance"""
        logger.info(f"TIMER: {operation_name} completed in {duration_ms:.2f}ms")


# Singleton instance
logger_manager = ProductionLogger()

def get_logger(module_name):
    """Convenience function to get logger"""
    return logger_manager.get_logger(module_name)
