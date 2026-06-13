# 🚀 Quick Start Guide

<div align="center">
  <a href="./README.md"><img src="./docs/assets/buttons/readme.svg" alt="Main README" height="38"></a>
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
     python -m src.fft_analyzer.cli.main analyze outputs/signal.csv --window  hann --fs 1000 --output-dir outputs/
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
1. Open the public browser URL: [https://fft-signal-analyzer.streamlit.app](https://fft-signal-analyzer.streamlit.app).
2. Generate synthetic signals using the sidebar sliders or upload your `.csv`, `.wav`, or `.npy` file.
3. Perform real-time FFT, noise filtering, peak detection, and interactive plotting immediately.

---

## 📋 File Layout Reference

* `streamlit_app.py` - Streamlit application entry point.
* `src/fft_analyzer/cli/main.py` - Core CLI entry point.
* `src/fft_analyzer/core/` - Reusable core signal processing library modules.
