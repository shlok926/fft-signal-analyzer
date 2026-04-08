"""
Session Management - Persistent state, history, and undo/redo
"""

import streamlit as st
from datetime import datetime
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

class SessionManager:
    """Manage Streamlit session state with persistence"""
    
    def __init__(self):
        self.history_dir = Path("session_history")
        self.history_dir.mkdir(exist_ok=True)
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize session state"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        if 'undo_stack' not in st.session_state:
            st.session_state.undo_stack = []
        
        if 'redo_stack' not in st.session_state:
            st.session_state.redo_stack = []
        
        if 'session_settings' not in st.session_state:
            st.session_state.session_settings = {
                'theme': 'dark',
                'auto_save': True,
                'notifications': True,
                'cache_enabled': True,
            }
        
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
    
    @staticmethod
    def add_to_history(action: str, data: Dict[str, Any]):
        """Add action to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data': data,
        }
        
        st.session_state.history.append(entry)
        
        # Keep only last 100 entries
        if len(st.session_state.history) > 100:
            st.session_state.history = st.session_state.history[-100:]
    
    @staticmethod
    def get_history(limit: int = 10) -> List[Dict]:
        """Get recent history"""
        return st.session_state.history[-limit:]
    
    @staticmethod
    def clear_history():
        """Clear all history"""
        st.session_state.history = []
    
    @staticmethod
    def push_undo(state: Dict[str, Any]):
        """Push state to undo stack"""
        st.session_state.undo_stack.append(state)
        st.session_state.redo_stack = []  # Clear redo when new action
    
    @staticmethod
    def undo() -> Optional[Dict]:
        """Undo last action"""
        if st.session_state.undo_stack:
            state = st.session_state.undo_stack.pop()
            st.session_state.redo_stack.append(state)
            return state
        return None
    
    @staticmethod
    def redo() -> Optional[Dict]:
        """Redo last undone action"""
        if st.session_state.redo_stack:
            state = st.session_state.redo_stack.pop()
            st.session_state.undo_stack.append(state)
            return state
        return None
    
    @staticmethod
    def save_session():
        """Save session to file"""
        session_file = Path("session_history") / f"session_{st.session_state.session_id}.json"
        
        try:
            session_data = {
                'session_id': st.session_state.session_id,
                'created_at': datetime.now().isoformat(),
                'analysis_count': st.session_state.analysis_count,
                'settings': st.session_state.session_settings,
                'history_count': len(st.session_state.history),
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"✅ Session saved: {session_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving session: {str(e)}")
            return False
    
    @staticmethod
    def get_setting(key: str, default: Any = None) -> Any:
        """Get session setting"""
        return st.session_state.session_settings.get(key, default)
    
    @staticmethod
    def set_setting(key: str, value: Any):
        """Set session setting"""
        st.session_state.session_settings[key] = value
    
    @staticmethod
    def increment_analysis_count():
        """Increment analysis counter"""
        st.session_state.analysis_count += 1
    
    @staticmethod
    def get_session_stats() -> Dict[str, Any]:
        """Get session statistics"""
        return {
            'session_id': st.session_state.session_id,
            'analyses_run': st.session_state.analysis_count,
            'history_entries': len(st.session_state.history),
            'undo_available': len(st.session_state.undo_stack) > 0,
            'redo_available': len(st.session_state.redo_stack) > 0,
        }


# Singleton instance
session_manager = SessionManager()

def get_session_manager() -> SessionManager:
    """Get session manager instance"""
    return session_manager
