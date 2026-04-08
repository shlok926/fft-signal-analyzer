#!/usr/bin/env python3
"""
Build script for FFT Spectrum Analyzer desktop application
Creates a standalone .exe using PyInstaller
"""

import PyInstaller.__main__
import sys
import os

# Define build parameters
APP_NAME = "FFT_Spectrum_Analyzer"
MAIN_SCRIPT = "streamlit_app.py"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"

# PyInstaller arguments
args = [
    MAIN_SCRIPT,
    f"--name={APP_NAME}",
    f"--distpath={OUTPUT_DIR}",
    "--workpath=build",
    "--onefile",
    "--windowed",
    "--icon=ICON.ico" if os.path.exists("ICON.ico") else "",
    "--add-data=src:src",
    "--add-data=config:config",
    "--add-data=.streamlit:.streamlit",
    "--hidden-import=streamlit",
    "--hidden-import=plotly",
    "--hidden-import=pandas",
    "--hidden-import=numpy",
    "--hidden-import=scipy",
    "--hidden-import=sklearn",
    "--collect-all=streamlit",
    "--collect-all=plotly",
    f"--splash=assets/splash.png" if os.path.exists("assets/splash.png") else "",
]

# Clean up empty strings
args = [arg for arg in args if arg]

print("=" * 70)
print("🚀 Building FFT Spectrum Analyzer Desktop Application")
print("=" * 70)
print(f"\nApp Name: {APP_NAME}")
print(f"Main Script: {MAIN_SCRIPT}")
print(f"Output Directory: {OUTPUT_DIR}")
print(f"\nPyInstaller Arguments:")
for arg in args:
    print(f"  {arg}")
print("\n" + "=" * 70)
print("Starting build process...")
print("=" * 70 + "\n")

try:
    PyInstaller.__main__.run(args)
    print("\n" + "=" * 70)
    print("✅ BUILD SUCCESSFUL!")
    print("=" * 70)
    print(f"\n📦 Executable location: {OUTPUT_DIR}\\{APP_NAME}.exe")
    print(f"📁 Full path: {os.path.abspath(os.path.join(OUTPUT_DIR, f'{APP_NAME}.exe'))}")
    print("\n✨ You can now run the app by double-clicking the .exe file!")
    print(f"\n💾 To distribute: Zip the '{OUTPUT_DIR}' folder and share")
    print("=" * 70)
except Exception as e:
    print("\n" + "=" * 70)
    print(f"❌ BUILD FAILED: {str(e)}")
    print("=" * 70)
    sys.exit(1)
