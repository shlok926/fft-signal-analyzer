#!/usr/bin/env python3
"""
Build FFT Spectrum Analyzer as standalone .exe using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """Build the executable"""
    
    print("\n" + "="*60)
    print("🔨 FFT Spectrum Analyzer - Desktop Build")
    print("="*60)
    
    # Paths
    project_root = Path(__file__).parent
    app_file = project_root / "streamlit_app.py"
    dist_folder = project_root / "dist"
    build_folder = project_root / "build"
    spec_file = project_root / "FFT_Spectrum_Analyzer.spec"
    
    # Check if streamlit_app.py exists
    if not app_file.exists():
        print(f"❌ Error: {app_file} not found!")
        sys.exit(1)
    
    print(f"\n📁 Project root: {project_root}")
    print(f"📄 App file: {app_file}")
    
    # Remove old build artifacts
    print("\n🧹 Cleaning old build artifacts...")
    for folder in [dist_folder, build_folder]:
        if folder.exists():
            shutil.rmtree(folder)
            print(f"   ✓ Removed {folder.name}/")
    
    if spec_file.exists():
        spec_file.unlink()
        print(f"   ✓ Removed {spec_file.name}")
    
    # Build command
    print("\n⚙️  Building executable with PyInstaller...")
    print("   This may take 2-5 minutes...")
    
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=FFT_Spectrum_Analyzer",
        "--onefile",
        "--windowed",
        "--icon=ICON.ico" if (project_root / "ICON.ico").exists() else "",
        "--add-data=src:src",
        "--add-data=config:config",
        "--hidden-import=streamlit",
        "--hidden-import=plotly",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=scipy",
        "--hidden-import=scikit-learn",
        "--collect-all=streamlit",
        "--collect-all=altair",
        str(app_file)
    ]
    
    # Remove empty strings
    build_cmd = [x for x in build_cmd if x]
    
    try:
        result = subprocess.run(build_cmd, cwd=project_root, check=True)
        
        # Check if exe was created
        exe_file = dist_folder / "FFT_Spectrum_Analyzer.exe"
        if exe_file.exists():
            exe_size_mb = exe_file.stat().st_size / (1024 * 1024)
            print(f"\n✅ Build successful!")
            print(f"   📦 Executable: {exe_file}")
            print(f"   📊 Size: {exe_size_mb:.1f} MB")
            print(f"\n🚀 To run: .\\dist\\FFT_Spectrum_Analyzer.exe")
            return True
        else:
            print(f"\n❌ Build failed: .exe file not found at {exe_file}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
