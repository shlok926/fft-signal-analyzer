# 🚀 FFT Spectrum Analyzer - Desktop Launcher Guide

## 👥 Who Should Use This?

**Perfect For:**
- 🔬 **Engineers & Scientists** - Signal processing, FFT analysis, frequency domain research
- 📊 **Data Analysts** - Time-series analysis, pattern detection, anomaly identification
- 🎵 **Audio Engineers** - Audio signal analysis, frequency spectrum visualization
- 📡 **Telecommunications** - Signal quality analysis, frequency monitoring
- 🤖 **ML Researchers** - Signal classification, compression, feature extraction
- 👨‍🎓 **Students** - Learning signal processing, FFT, digital filters
- 💼 **Professionals** - Quality control, diagnostics, equipment monitoring

**Features Suitable For:**
| Use Case | Feature |
|----------|---------|
| Audio Analysis | Frequency spectrum, spectrogram |
| Vibration Detection | Peak detection, anomaly detection |
| Signal Compression | Data compression with energy preservation |
| Quality Assurance | Statistical analysis, classification |
| Research | Multiple export formats, AI-powered analysis |

**Capability Matrix:**

```
                    Audio  Mech  Data   Research QC   Students
Signal Import       ✅    ✅    ✅     ✅       ✅    ✅
FFT Analysis        ✅    ✅    ✅     ✅       ✅    ✅
Peak Detection      ✅    ✅    ✅     ✅       ✅    ✅
Digital Filters     ✅    ✅    ✅     ✅       ✅    ✅
Spectrogram         ✅    ✅    ✅     ✅       ✅    ✅
Compression         ⭐    ⭐    ✅     ✅       ✅    ✅
Anomaly Detection   ⭐    ✅    ✅     ✅       ✅    ⭐
Classification      ⭐    ✅    ✅     ✅       ✅    ⭐
Statistics          ✅    ✅    ✅     ✅       ✅    ✅
Excel Export        ✅    ✅    ✅     ✅       ✅    ✅

Legend: ✅ = Useful   ⭐ = Highly Recommended
```

---

## Quick Start

### Option 1: Desktop Shortcut (Easiest)
1. **Look on your Desktop** for "FFT Spectrum Analyzer.lnk"
2. **Double-click** to launch the app
3. Browser will open automatically at `http://localhost:8501`

### Option 2: Run the Batch File
1. Open File Explorer
2. Navigate to: `c:\Users\Shlok\fft_signal_analyzer\`
3. Double-click: `FFT_Spectrum_Analyzer.bat`
4. Wait for the app to start (~5-10 seconds on first run)

### Option 3: Command Line
```powershell
cd c:\Users\Shlok\fft_signal_analyzer
streamlit run streamlit_app.py
```

## What Happens on First Launch

1. ✅ Dependencies are checked/installed automatically
2. ⏳ Streamlit server starts (takes 5-10 seconds)
3. 🌐 Browser opens at `http://localhost:8501`
4. 📡 App is ready to use

## How to Use

### Generate Signal
- Set frequency, amplitude, and noise parameters
- Click "▶️ ANALYZE" button
- View real-time plots and analysis

### Import Signal
- Click "📁 Import File" tab
- Upload `.csv`, `.wav`, or `.npy` file
- Specify sampling rate (if needed)
- Click "▶️ ANALYZE"

### Export Results
- Generate analysis by clicking "ANALYZE"
- Click "⬇️ EXPORT" button
- Download Excel file with spectrum data and peaks

### AI Features
After analysis, use:
- **🗜️ Data Compression** - Compress spectrum while keeping key data
  - *For:* Data storage, bandwidth optimization, research
- **🚨 Anomaly Detection** - Find unusual frequencies
  - *For:* Equipment monitoring, quality control, fault detection
- **🧠 Signal Classification** - Identify signal type
  - *For:* Automatic signal categorization, pattern recognition

## Features

✨ **Real-Time Signal Processing**
- Generate or import signals
- Apply digital filters (low-pass, high-pass, band-pass, notch)
- Multiple window functions (Hann, Hamming, Blackman, Kaiser, etc.)

📊 **Advanced Analysis**
- Frequency spectrum (FFT)
- Phase spectrum
- Power spectral density (PSD)
- Time-frequency spectrogram
- Statistical analysis

🤖 **AI-Powered Tools**
- Signal compression with frequency selection
- Anomaly detection using Isolation Forest
- Neural network signal classification
- Compression metrics and energy preservation

💾 **Export Options**
- Excel files with spectrum data and peak list
- Supports multiple sheets

## System Requirements

- Windows 10 or 11
- Python 3.11+ (installed separately from python.org)
- 2GB RAM minimum
- Modern web browser

## Troubleshooting

### "Python is not installed"
- Download from: https://www.python.org/downloads/
- **Make sure to check "Add Python to PATH"** during installation
- Restart computer after installation

### Port already in use
- If you see "Address already in use", close other Streamlit instances
- Or use custom port: `streamlit run streamlit_app.py --server.port 8502`

### App runs slow on first launch
- First startup needs 5-10 seconds to initialize Streamlit
- Subsequent runs are faster
- Ensure you have at least 2GB free RAM

### Browser doesn't open
- Manually open: `http://localhost:8501`
- If nothing appears after 30 seconds, restart the batch file

## GitHub Repository

Code and updates available at:
https://github.com/shlok926/fft-signal-analyzer

## 🎯 User Personas & Use Cases

### 1. **Audio Engineers**
- ✅ Import audio files (.wav)
- ✅ Analyze frequency content
- ✅ Detect audio artifacts and anomalies
- ✅ Export spectrum analysis

### 2. **Mechanical Engineers**
- ✅ Vibration analysis from sensors
- ✅ Bearing fault detection (anomaly detection)
- ✅ Equipment health monitoring
- ✅ Identify mechanical resonances

### 3. **Data Scientists**
- ✅ Feature extraction from signals
- ✅ Data compression for ML pipelines
- ✅ Time-series analysis
- ✅ Signal classification models

### 4. **Researchers & Academics**
- ✅ Signal processing experiments
- ✅ FFT algorithm testing
- ✅ Filter design and validation
- ✅ Publication-ready plots and data

### 5. **Quality Control Specialists**
- ✅ Equipment testing and validation
- ✅ Anomaly detection in production
- ✅ Statistical signatures
- ✅ Excel export for reporting

### 6. **Students & Learners**
- ✅ Learn FFT and signal processing
- ✅ Interactive visualization
- ✅ Multiple filter types to experiment
- ✅ Real-time feedback

## Support

For issues, check:
1. The GitHub issues page
2. Console output in the batch file for error messages
3. Verify all dependencies are installed (see batch file output)

---

**Version:** 1.0  
**Last Updated:** April 2026  
**Built with:** Streamlit, NumPy, SciPy, Plotly, Scikit-Learn
