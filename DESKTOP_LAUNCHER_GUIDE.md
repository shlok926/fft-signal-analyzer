# 🚀 FFT Spectrum Analyzer - Desktop Launcher Guide

## Quick Start (3 Methods)

### 1️⃣ **Desktop Shortcut** (Easiest)
- Look on your Desktop for: **"FFT Spectrum Analyzer.lnk"**
- Double-click to launch
- Browser opens automatically at `http://localhost:8501`

### 2️⃣ **Batch File Launcher**
```bash
Double-click: FFT_Spectrum_Analyzer.bat
```
- Auto-checks dependencies
- Starts Streamlit server
- Opens browser

### 3️⃣ **Command Line**
```bash
cd c:\Users\Shlok\fft_signal_analyzer
streamlit run streamlit_app.py
```

---

## ⏱️ What Happens on First Launch?

```
1. Python check ✅
2. Dependencies scan ✅
3. Auto-install if missing ⏳ (30-60 sec)
4. Streamlit starts 🚀
5. Browser opens 🌐
6. Ready to analyze! 📊
```

---

## 👥 Who Should Use This?

### 🔬 Engineers & Researchers
- RF Engineers
- DSP Engineers
- Electrical Engineers
- Mechanical Engineers (vibration analysis)

### 📊 Data Scientists & Analysts
- Time-series analysis
- Feature extraction
- Signal processing pipelines
- ML preprocessing

### 🎵 Audio Professionals
- Audio engineers
- Acousticians
- Sound designers
- Music producers

### 📡 Telecommunications
- Signal quality analysis
- Frequency monitoring
- Network diagnostics
- Equipment testing

### 👨‍🎓 Students & Educators
- Learning DSP
- FFT algorithms
- Signal processing
- Frequency analysis

### 💼 Quality Control
- Equipment validation
- Anomaly detection
- Diagnostics
- Compliance testing

---

## 🎯 Key Features for Each User

| User Type | Best Features |
|-----------|--------------|
| Audio Engineer | Spectrogram, Anomaly Detection, Phase Analysis |
| Mechanical Engineer | Peak Detection, Anomaly Detection, Compression |
| Data Scientist | Compression, Classification, Export |
| Researcher | All Features, Multi-window support |
| QC Engineer | Peak Detection, Anomaly Detection, Export |
| Student | All Features, Interactive Visualization |

---

## 💡 How to Use

### Basic Workflow
```
1. Generate or Import Signal
   └─ Set frequency, amplitude, noise
   └─ Or upload CSV/WAV/NPY file

2. Configure Analysis
   └─ Choose window function
   └─ Optional: Add filter

3. Click ANALYZE
   └─ FFT computation
   └─ Peak detection

4. Explore Results
   └─ 4 plots: Time, Frequency, Phase, PSD
   └─ Peak table
   └─ Statistics

5. Use AI Features (Optional)
   └─ Compress data
   └─ Detect anomalies
   └─ Classify signal

6. Export Results
   └─ Excel file with data
   └─ Ready for further analysis
```

---

## 🔧 System Requirements

| Item | Requirement |
|------|------------|
| OS | Windows 10/11 |
| Python | 3.11+ |
| RAM | 2GB minimum |
| Browser | Modern (Chrome, Edge, Firefox) |
| Disk | 500MB free |

---

## 📖 Documentation

- **Quick Start:** This file
- **Main README:** See repository overview
- **Code Examples:** In GitHub repository
- **API Reference:** In source code comments

---

## ❓ Troubleshooting

### "Python not found"
```
✅ Install Python 3.11+ from python.org
✅ Make sure "Add to PATH" is checked
✅ Restart computer after installation
```

### "Port 8501 already in use"
```
✅ Solution 1: Close other Streamlit instances
✅ Solution 2: Use custom port:
   streamlit run streamlit_app.py --server.port 8502
```

### "App runs slow first time"
```
✅ First launch: 5-10 seconds (normal)
✅ Subsequent: 1-2 seconds (cached)
✅ Just wait, it's initializing!
```

### "Browser doesn't open"
```
✅ Manual open: http://localhost:8501
✅ If still nothing, check console output
✅ Restart the batch file
```

### "Streamlit warnings appear"
```
✅ These are safe warnings
✅ App still works fine
✅ Can be ignored
```

---

## 💾 Next Steps

### 1. **Try a Demo**
- Generate 50Hz + 120Hz signal
- Click ANALYZE
- View the FFT result
- Great for learning!

### 2. **Analyze Your Data**
- Click "Import File"
- Upload your CSV/WAV
- Get instant frequency analysis

### 3. **Use AI Features**
- Compress spectrum (70% reduction)
- Detect anomalies
- Classify signal type

### 4. **Export Results**
- Click EXPORT
- Download Excel file
- Use in other tools

---

## 🔗 Resources

- **GitHub:** https://github.com/shlok926/fft-signal-analyzer
- **Issues/Bugs:** Create GitHub issue
- **Feature Requests:** GitHub discussions
- **Documentation:** See README.md

---

## 🎓 Learning Tips

```
1. START SIMPLE
   └─ Generate single frequency
   └─ Understand FFT output

2. EXPERIMENT
   └─ Add multiple frequencies
   └─ Try different windows
   └─ Apply filters

3. ANALYZE REAL DATA
   └─ Import your signal
   └─ Explore the spectrum
   └─ Find patterns

4. USE AI FEATURES
   └─ Compress large datasets
   └─ Detect anomalies
   └─ Classify signals
```

---

## 📞 Support

- 📝 Issues? Open GitHub issue
- 💬 Questions? GitHub discussions
- ⭐ Liked it? Star the repository!
- 📢 Share with others!

---

<div align="center">

**Made with ❤️ for signal processing enthusiasts**

[⬆ Back to Top](#-fft-spectrum-analyzer---desktop-launcher-guide)

</div>
