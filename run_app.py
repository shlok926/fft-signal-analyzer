import os
import sys
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # Get the directory where PyInstaller extracts files in onefile mode (_MEIPASS)
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    # Path to streamlit_app.py
    app_path = os.path.join(base_path, 'streamlit_app.py')
    
    # Set the arguments for Streamlit CLI
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.port=8501",
        "--server.headless=false"
    ]
    
    # Run Streamlit CLI
    sys.exit(stcli.main())
