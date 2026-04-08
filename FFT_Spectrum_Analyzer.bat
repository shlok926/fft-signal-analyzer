@echo off
REM ============================================================================
REM FFT Spectrum Analyzer - Windows Launcher
REM ============================================================================

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit -q
)

REM Check if required packages are installed
python -c "import plotly, pandas, numpy, scipy, scikit-learn" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install plotly pandas numpy scipy scikit-learn -q
)

REM Change to script directory
cd /d "!SCRIPT_DIR!"

REM Run the Streamlit app
echo.
echo ============================================================================
echo 📡 FFT Spectrum Analyzer
echo ============================================================================
echo.
echo Starting application...
echo Browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

timeout /t 2

REM Launch Streamlit
python -m streamlit run streamlit_app.py --logger.level=warning

pause
