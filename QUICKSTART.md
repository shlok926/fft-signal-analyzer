# 🚀 Quick Start Guide

<div align="center">
  <a href="./README.md"><img src="./docs/assets/buttons/readme.svg" alt="Main README" height="38"></a>
  <a href="./DESKTOP_LAUNCHER_GUIDE.md"><img src="./docs/assets/buttons/desktop_guide.svg" alt="Desktop App Guide" height="38"></a>
  <a href="https://github.com/shlok926/fft-signal-analyzer"><img src="./docs/assets/buttons/source_code.svg" alt="GitHub Repository" height="38"></a>
</div>

<br/>

This guide helps you choose the right format based on your profile, setup requirements, and use case.

---

## 📋 Comparison & Choose Your Format

| End-Product Format | Target Audience | Setup Requirements | Main Advantage | Quick Start Link |
| :--- | :--- | :--- | :--- | :--- |
| 🛠️ **1. The Tool (CLI/Lib)** | Developers, Researchers & Engineers | Python environment must be installed | Complete programming access & scriptability | [Go to Section ↓](#-1-the-tool-clilib) |
| 🌐 **2. The Web App (Cloud)** | Public, Educators, Students & Mobile Users | Zero installation (web browser only) | Run instantly on any device (incl. mobile) | [Go to Section ↓](#-2-the-web-app-cloud) |
| 💻 **3. The Desktop App (.exe)** | General/Offline Desktop Users | No Python needed (double-click to run) | Full offline privacy, local execution | [Go to Section ↓](#-3-the-desktop-app-exe) |

---

## 🛠️ 1. The Tool (CLI/Lib)
*For developers, researchers, and engineers seeking CLI scriptability, integration, or custom Python code development.*

### Setup Prerequisites:
* Python 3.11+ installed.
* Pip/Poetry package manager.

### Steps to Run:
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Use the Command Line Interface (CLI):**
   * **Verify Installation:**
     ```bash
     python -m src.fft_analyzer.cli.main version
     ```
   * **Generate a Signal:**
     ```bash
     python -m src.fft_analyzer.cli.main generate --freq 50 --freq 120 --fs 1000 --duration 1.0 --output outputs/signal.csv
     ```
   * **Analyze & Extract Peaks:**
     ```bash
     python -m src.fft_analyzer.cli.main analyze outputs/signal.csv --window hann --fs 1000 --output-dir outputs/
     ```
3. **Use as a Python Library:**
   You can import the core engines directly in your scripts:
   ```python
   from src.fft_analyzer.core import FFTEngine, SignalGenerator
   # Your signal analysis logic here...
   ```

---

## 🌐 2. The Web App (Cloud)
*For public users, educators, students, and mobile users looking for instant, zero-installation access to the signal analyzer.*

### Setup Prerequisites:
* **None!** Just a standard web browser (Chrome, Edge, Safari, Firefox).
* Internet connection.

### Steps to Run:
1. Open the public browser URL: [https://fft-analyzer.streamlit.app](https://fft-analyzer.streamlit.app) *(or your deployed cloud service)*.
2. Generate synthetic signals using the sidebar sliders or upload your `.csv`, `.wav`, or `.npy` file.
3. Perform real-time FFT, noise filtering, peak detection, and interactive plotting immediately.

---

## 💻 3. The Desktop App (.exe)
*For general/offline desktop users who want to run the application locally without managing Python, dependencies, or command lines.*

### Setup Prerequisites:
* **None!** (No Python or packages required on target machines).
* Windows 10/11 system.

### Steps to Run:
1. Go to the project's **GitHub Releases** page.
2. Download the `FFT_Spectrum_Analyzer.exe` file.
3. Double-click the file to launch it!
   * *A console helper window and default browser session will open at `http://localhost:8501` automatically.*

### How to Compile locally (for Developers):
If you want to compile the standalone `.exe` yourself:
```bash
python build_exe.py
```
This cleans the build directories and generates a single self-contained executable file under `dist/FFT_Spectrum_Analyzer.exe` using PyInstaller.

---

## 📋 File Layout Reference

* `streamlit_app.py` - Streamlit application entry point.
* `build_exe.py` - Script to bundle Streamlit & code into a single offline `.exe`.
* `src/fft_analyzer/cli/main.py` - Core CLI entry point.
* `src/fft_analyzer/core/` - Reusable core signal processing library modules.
