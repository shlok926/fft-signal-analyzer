"""
Error Handling & Caching System
"""

import functools
import time
from typing import Any, Callable, Optional, Dict
from datetime import datetime, timedelta
import hashlib
import json

class ErrorHandler:
    """Comprehensive error handling system"""
    
    @staticmethod
    def safe_call(func: Callable, *args, default=None, logger=None, context=""):
        """
        Safely call a function with error handling
        
        Args:
            func: Function to call
            args: Function arguments
            default: Default value on error
            logger: Logger instance
            context: Error context message
        
        Returns:
            Function result or default value
        """
        try:
            return func(*args)
        except Exception as e:
            error_msg = f"Error in {context or func.__name__}: {str(e)}"
            if logger:
                logger.error(error_msg)
            else:
                print(f"❌ {error_msg}")
            return default
    
    @staticmethod
    def validate_input(value: Any, expected_type: type, name: str, logger=None) -> bool:
        """Validate input parameter"""
        if not isinstance(value, expected_type):
            msg = f"Invalid {name}: expected {expected_type.__name__}, got {type(value).__name__}"
            if logger:
                logger.error(msg)
            else:
                print(f"❌ {msg}")
            return False
        return True
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float, name: str, logger=None) -> bool:
        """Validate value is in range"""
        if not (min_val <= value <= max_val):
            msg = f"{name} must be between {min_val} and {max_val}, got {value}"
            if logger:
                logger.error(msg)
            else:
                print(f"❌ {msg}")
            return False
        return True


class CacheManager:
    """Memory cache with TTL (Time-To-Live)"""
    
    _instance = None
    _cache: Dict[str, Dict[str, Any]] = {}
    _enabled = True
    _ttl_seconds = 3600  # 1 hour default
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, enabled: bool = True, ttl_seconds: int = 3600):
        self._enabled = enabled
        self._ttl_seconds = ttl_seconds
    
    @staticmethod
    def _make_key(func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key from function name and arguments"""
        key_data = f"{func_name}_{str(args)}_{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._enabled or key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if datetime.now() > entry['expires_at']:
            del self._cache[key]
            return None
        
        entry['hits'] += 1
        return entry['value']
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Store value in cache"""
        if not self._enabled:
            return
        
        ttl = ttl_seconds or self._ttl_seconds
        
        self._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl),
            'created_at': datetime.now(),
            'hits': 0,
        }
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_hits = sum(entry['hits'] for entry in self._cache.values())
        
        return {
            'enabled': self._enabled,
            'total_entries': len(self._cache),
            'total_hits': total_hits,
            'memory_estimate_mb': sum(len(str(entry['value'])) for entry in self._cache.values()) / (1024*1024),
        }
    
    def cleanup_expired(self):
        """Remove expired entries"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if datetime.now() > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)
    
    @staticmethod
    def cached(ttl_seconds: int = 3600):
        """Decorator to cache function results"""
        cache = CacheManager()
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key = CacheManager._make_key(func.__name__, args, kwargs)
                
                # Try to get from cache
                cached_value = cache.get(key)
                if cached_value is not None:
                    print(f"💾 Cache hit: {func.__name__}")
                    return cached_value
                
                # Calculate and cache
                result = func(*args, **kwargs)
                cache.set(key, result, ttl_seconds)
                
                return result
            
            return wrapper
        
        return decorator


# Singleton instances
error_handler = ErrorHandler()
cache_manager = CacheManager()

def safe_execute(func: Callable, *args, **kwargs):
    """Convenience function for safe execution"""
    return error_handler.safe_call(func, *args, **kwargs)

@CacheManager.cached(ttl_seconds=3600)
def cached_operation(data):
    """Example cached operation"""
    return data
