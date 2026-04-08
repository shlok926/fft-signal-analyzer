"""
Configuration Manager - YAML-based config with validation
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import json

class ConfigManager:
    """Manage application configuration from YAML/JSON files"""
    
    _instance = None
    _config = {}
    _config_file = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config_file: Optional[str] = None):
        if not self._config:
            self.load_config(config_file)
    
    def load_config(self, config_file: Optional[str] = None):
        """Load configuration from YAML or JSON file"""
        
        # Try to find config file
        if config_file is None:
            # Look in standard locations
            candidates = [
                Path("config/config.yaml"),
                Path("config/config.dev.yaml"),
                Path("config.yaml"),
            ]
            
            for candidate in candidates:
                if candidate.exists():
                    config_file = str(candidate)
                    break
        
        if config_file and Path(config_file).exists():
            self._config_file = config_file
            
            try:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    with open(config_file, 'r') as f:
                        self._config = yaml.safe_load(f) or {}
                elif config_file.endswith('.json'):
                    with open(config_file, 'r') as f:
                        self._config = json.load(f)
                
                print(f"[OK] Config loaded from {config_file}")
            except Exception as e:
                print(f"[WARN] Error loading config: {str(e)}")
                self._config = {}
        else:
            print("[WARN] No config file found, using defaults")
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration"""
        self._config = {
            'app': {
                'name': 'FFT Signal Analyzer',
                'version': '1.0.0',
                'debug': False,
            },
            'signal': {
                'default_fs': 1000,
                'default_duration': 1.0,
                'min_samples': 10,
                'max_samples': 1000000,
            },
            'fft': {
                'window_functions': ['hann', 'hamming', 'blackman', 'rectangle', 'bartlett', 'kaiser'],
                'default_window': 'hann',
                'zero_padding': True,
            },
            'export': {
                'max_file_size_mb': 100,
                'pdf_enabled': True,
                'png_enabled': True,
                'matlab_enabled': True,
            },
            'performance': {
                'cache_enabled': True,
                'cache_ttl_seconds': 3600,
                'max_memory_mb': 500,
            },
            'logging': {
                'level': 'INFO',
                'file_enabled': True,
                'console_enabled': True,
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot notation (e.g., 'signal.default_fs')"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set config value by dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, filepath: Optional[str] = None):
        """Save current config to file"""
        target = filepath or self._config_file or "config.yaml"
        
        try:
            with open(target, 'w') as f:
                if target.endswith('.json'):
                    json.dump(self._config, f, indent=2)
                else:
                    yaml.dump(self._config, f, default_flow_style=False)
            
            print(f"✅ Config saved to {target}")
        except Exception as e:
            print(f"❌ Error saving config: {str(e)}")
    
    def to_dict(self) -> Dict:
        """Get entire config as dictionary"""
        return self._config.copy()
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_keys = ['app', 'signal', 'fft', 'export']
        
        for key in required_keys:
            if key not in self._config:
                print(f"⚠️ Missing required config section: {key}")
                return False
        
        return True


# Singleton instance
config_manager = ConfigManager()

def get_config(key: str, default: Any = None) -> Any:
    """Convenience function to get config value"""
    return config_manager.get(key, default)

def set_config(key: str, value: Any):
    """Convenience function to set config value"""
    config_manager.set(key, value)
