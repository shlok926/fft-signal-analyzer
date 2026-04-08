# 📡 FFT Signal Analyzer

> **Real-Time Signal Processing & Frequency Domain Analysis**

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   Professional FFT Analysis Tool for Engineers & Researchers    ║
║                                                                  ║
║   • Interactive Dashboard • Real-time Analysis • AI Features    ║
║   • Multiple Export Formats • Peak Detection • Signal Filtering  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🎯 What is FFT Signal Analyzer?

A **production-ready, AI-enhanced signal processing application** for frequency domain analysis, spectral examination, and intelligent signal classification.

**Perfect for:**
- 🔬 Signal Processing Research
- 📊 Audio & Vibration Analysis  
- 🎵 Acoustic Engineering
- 📡 Telecommunications
- 🤖 AI/ML Feature Extraction
- 👨‍🎓 Educational Learning

---

## ✨ Key Features

### 🎚️ Signal Processing
| Feature | Capability |
|---------|-----------|
| **Signal Generation** | Composite signals with multiple frequencies + configurable noise |
| **FFT Computation** | 6 window functions (Hann, Hamming, Blackman, Kaiser, Rectangle, Bartlett) |
| **Digital Filtering** | Low-pass, High-pass, Band-pass, Notch (Butterworth, zero-phase) |
| **Peak Detection** | Automatic detection with prominence thresholds |

### 📈 Visualization & Analysis
- ✅ Time-domain waveform display
- ✅ Frequency spectrum (magnitude, magnitude-dB, phase)
- ✅ Power Spectral Density (PSD)
- ✅ Time-Frequency Spectrogram
- ✅ Statistical analysis (mean, RMS, peak, skewness, kurtosis)
- ✅ Interactive Plotly dashboard

### 🤖 AI-Powered Features
- **🗜️ Data Compression** - Frequency-based spectrum compression with energy preservation
- **🚨 Anomaly Detection** - Isolation Forest-based frequency anomaly detection
- **🧠 Signal Classification** - Neural network classification (Normal, Periodic, Transient, Chaotic, Noisy)

### 💾 Export & Integration
- ✅ Excel export with multiple sheets (Spectrum, Peaks)
- ✅ CSV data export
- ✅ WAV/NPY file import
- ✅ Batch processing capability

---

## 🛠️ Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│  BACKEND          │  FRONTEND      │  ANALYSIS         │
│  ─────────────    │  ──────────    │  ────────────     │
│  Python 3.11+    │  Streamlit     │  NumPy            │
│  SciPy           │  Plotly        │  SciPy            │
│  NumPy           │  HTML/CSS      │  Scikit-learn     │
│  Pandas          │                │  TensorFlow/Keras │
└─────────────────────────────────────────────────────────┘
```

### Dependencies
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Latest-013243?logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

---

## 🚀 Quick Start

### ⚡ Fastest Way (Recommended)

**Option 1: Desktop Shortcut**
```bash
Double-click: "FFT Spectrum Analyzer" shortcut on desktop
```

**Option 2: Batch Launcher**
```bash
c:\Users\Shlok\fft_signal_analyzer\FFT_Spectrum_Analyzer.bat
```

**Option 3: Command Line**
```bash
cd c:\Users\Shlok\fft_signal_analyzer
streamlit run streamlit_app.py
```

✨ **First Launch Magic:**
- ✅ Dependencies auto-check & install
- ✅ Streamlit server starts automatically
- ✅ Browser opens at `http://localhost:8501`
- ✅ Ready to analyze signals!

---

## 📖 Installation

### Prerequisites
- **Python 3.11+** (Download from [python.org](https://www.python.org))
- **pip** (comes with Python)
- **2GB RAM** minimum
- **Modern web browser**

### Step 1: Clone Repository
```bash
git clone https://github.com/shlok926/fft-signal-analyzer.git
cd fft-signal-analyzer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
streamlit run streamlit_app.py
```

✨ That's it! Your browser opens at `http://localhost:8501`

---

## 💡 How to Use

### 🎯 Step-by-Step Guide

#### 1️⃣ **Generate or Import a Signal**

**Method A: Generate Test Signal**
- Set **Frequency 1** & **Frequency 2** (Hz)
- Set **Amplitude 1** & **Amplitude 2**
- Add **Noise** (SNR dB slider)
- Set **Sampling Rate** (Hz)
- Set **Duration** (seconds)

**Method B: Import Your Data**
- Click **"📁 Import File"** tab
- Upload `.csv`, `.wav`, or `.npy` file
- Specify sampling rate if needed

#### 2️⃣ **Configure Analysis**

- Choose **Window Function**: Hann (default), Hamming, Blackman, Kaiser, etc.
- **Optional Filters**: Low-pass, High-pass, Band-pass, Notch
- Set **Filter Cutoff Frequency**

#### 3️⃣ **Click ANALYZE**

```
Input Signal → FFT → Peak Detection → Results
     ↓          ↓         ↓            ↓
   1000 pts    1000 freqs 20 peaks   4 plots
```

#### 4️⃣ **Explore Results**

- 📈 **Time-Domain Plot** - Raw signal waveform
- 📊 **Frequency Spectrum** - Magnitude at each frequency
- 🔄 **Phase Spectrum** - Phase angles
- ⚡ **Power Spectral Density** - Energy distribution

#### 5️⃣ **Use AI Features**

| Feature | Use Case |
|---------|----------|
| 🗜️ **Compression** | Reduce data size, keep important frequencies |
| 🚨 **Anomaly Detection** | Find unusual frequency spikes |
| 🧠 **Classification** | Identify signal type automatically |

#### 6️⃣ **Export Results**

- ✅ Click **"⬇️ EXPORT"** button
- 📊 Download **Excel file** with:
  - Spectrum data (frequency, magnitude, phase, PSD)
  - Top 20 detected peaks
- 💾 Ready for further analysis

---

## 🎓 Example Use Cases

### 🎵 Audio Engineer
```
1. Import audio.wav file
2. Analyze frequency content
3. Detect audio artifacts (anomalies)
4. Export spectrum for report
```

### 🔧 Mechanical Engineer  
```
1. Import vibration data from sensor
2. Find dominant frequencies
3. Use anomaly detection for fault detection
4. Export for maintenance report
```

### 📊 Data Scientist
```
1. Generate test signals
2. Apply compression (70% reduction)
3. Extract features for ML
4. Export for model training
```

### 👨‍🎓 Student
```
1. Generate 50Hz + 120Hz signal
2. Apply Hann window
3. View FFT result
4. Learn frequency analysis
```

---

## 📂 Project Structure

```
fft_signal_analyzer/
│
├── 📄 streamlit_app.py              ⭐ Main application
│
├── src/fft_analyzer/
│   ├── core/                        🔧 DSP algorithms
│   │   ├── signal_generator.py      └─ Generate signals
│   │   ├── fft_engine.py            └─ FFT computation
│   │   ├── filter_engine.py         └─ Digital filters
│   │   └── peak_detector.py         └─ Peak detection
│   │
│   ├── ai/                          🤖 AI Features
│   │   ├── compression_engine.py    └─ Data compression
│   │   ├── anomaly_detector.py      └─ Anomaly detection
│   │   └── signal_classifier.py     └─ Signal classification
│   │
│   ├── visualization/               📊 Plotting & analysis
│   │   ├── freq_domain_plot.py
│   │   ├── time_domain_plot.py
│   │   └── visualizer.py
│   │
│   ├── export/                      💾 Export formats
│   │   ├── csv_exporter.py
│   │   └── pdf_exporter.py
│   │
│   ├── utils/                       🛠️ Helpers
│   │   ├── logger.py
│   │   ├── config_manager.py
│   │   └── validators.py
│   │
│   └── models/                      📦 Data classes
│       ├── signal_data.py
│       └── spectrum_data.py
│
├── config/                          ⚙️ Configuration
│   └── config.yaml
│
├── tests/                           ✅ Unit & integration tests
│   ├── unit/
│   └── integration/
│
├── requirements.txt                 📋 Dependencies
├── QUICKSTART.md                    🚀 Quick start guide
├── FFT_Spectrum_Analyzer.bat        🖱️ Windows launcher
└── README.md                        📖 This file
```

---

## ❓ FAQ & Troubleshooting

### Q: App won't start?
```bash
❌ Error: "Python not found"
✅ Solution: Install Python 3.11+ from python.org

❌ Error: "Port 8501 already in use"
✅ Solution: streamlit run streamlit_app.py --server.port 8502

❌ Error: "Missing module streamlit"
✅ Solution: pip install -r requirements.txt
```

### Q: First launch is slow?
```
Streamlit starts in 5-10 seconds first time
Subsequent launches are faster (cached)
This is normal! ⏳
```

### Q: How do I analyze my own data?
```bash
1. Click "📁 Import File" tab
2. Upload CSV, WAV, or NPY file
3. Specify sampling frequency
4. Click ANALYZE
Done! 🎉
```

### Q: What's the recommended sampling rate?
```
Nyquist Theorem: fs > 2 × max_frequency
Common values:
  - 44.1 kHz (Audio)
  - 48 kHz (Professional audio)
  - 1 kHz (Industrial signals)
  - 100 Hz (Vibration)
```

### Q: How accurate is peak detection?
```
Depends on:
✅ Window function (Hann is default, best for most)
✅ Zero-padding (enabled by default)
✅ Signal SNR (higher SNR = more accurate)
✅ Peak prominence threshold
```

### Q: Can I export to other formats?
```
Current: ✅ Excel, CSV
Future: PDF, PNG images (coming soon)
```

## Documentation

### Key Modules

#### SignalGenerator
Generate synthetic signals with multiple frequency components and configurable noise.

```python
signal = SignalGenerator.generate_signal(
    components=[{"frequency": 50, "amplitude": 1.0, "phase": 0}],
    fs=1000,
    duration=1.0,
    snr_db=20,
)
```

#### FFTEngine
Compute FFT with windowing, zero-padding, and automatic frequency axis generation.

```python
spectrum = FFTEngine.compute_fft(signal, window_type="hann", zero_pad=True)
# Returns: SpectrumData with magnitude, magnitude_db, phase, psd, freqs
```

#### FilterEngine
Apply digital filters (Butterworth IIR, zero-phase).

```python
filtered = FilterEngine.low_pass(signal, cutoff_hz=200, order=4)
```

#### PeakDetector
Automatically detect dominant peaks with prominence-based filtering.

```python
peaks = PeakDetector.detect_peaks(spectrum, height_threshold=0.05, prominence_factor=0.1)
```

#### Visualizer
Create interactive Plotly plots for all analysis views.

```python
fig = Visualizer.plot_frequency_domain(spectrum, peaks)
fig.show()
```

#### Exporter
Save results to multiple formats.

```python
Exporter.export_all(
    "outputs",
    spectrum_data=spectrum,
    peaks=peaks,
    figures={"freq_plot": fig},
)
```

---

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

```yaml
signal:
  sampling_rate: 1000      # Hz
  duration: 1.0            # Seconds
  components:
    - frequency: 50        # Hz
      amplitude: 1.0
      
fft:
  window: "hann"           # Window function
  zero_padding: true       # Improves resolution

filter:
  enabled: false
  type: "lowpass"
  cutoff_hz: 200
  order: 4

peaks:
  prominence_factor: 0.1   # Sensitivity
  min_distance_hz: 5       # Minimum separation
```

---

## 🔬 Technical Details

### FFT Algorithm
```
Method:      Cooley-Tukey Radix-2 FFT (via NumPy)
Precision:   64-bit floating point
Windows:     Hann, Hamming, Blackman, Kaiser, Rectangle
Zero-pad:    Automatic to next power of 2
Spectrum:    One-sided, normalized
```

### Digital Filtering
```
Algorithm:   Butterworth IIR (SciPy)
Order:       Default 4th order
Zero-phase:  sosfiltfilt (symmetric)
Types:       LP, HP, BP, Notch
```

### Peak Detection
```
Algorithm:   scipy.signal.find_peaks()
Metrics:     Height, Prominence, Distance
Output:      Frequency, Magnitude, Prominence
```

### AI Algorithms
```
Compression:         Frequency selection with energy threshold
Anomaly Detection:   Isolation Forest (scikit-learn)
Classification:      Neural Network (TensorFlow/Keras)
```

---

## 📊 Performance Metrics

**Typical Processing Time (Modern Hardware):**

| FFT Size | Time | Comment |
|----------|------|---------|
| 1,024 | <1 ms | Instant |
| 65,536 | <10 ms | Very fast |
| 1,048,576 | <500 ms | Fast |
| 10,000,000 | <5 sec | Acceptable |

**Memory Usage:**
```
Signal size: 1M points     ≈ 8 MB
FFT result:  512K freqs    ≈ 4 MB
Total:                     ≈ 20 MB (with overhead)
```

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

### 1. **Report Issues**
- Found a bug? Open an Issue with:
  - Clear description
  - Steps to reproduce
  - Screenshot/error message

### 2. **Suggest Features**
- Have an idea? Open an Issue (prefix with `[FEATURE]`)
- Describe the use case
- Explain the benefits

### 3. **Submit Code**
```bash
1. Fork the repository
2. Create feature branch: git checkout -b feature/awesome-feature
3. Commit changes: git commit -m "Add awesome feature"
4. Push to branch: git push origin feature/awesome-feature
5. Open Pull Request
```

### 4. **Run Tests Before Submitting**
```bash
# Ensure code quality
pytest tests/
```

---

## 📜 License

**MIT License** - See [LICENSE](LICENSE) file

You are free to:
- ✅ Use commercially
- ✅ Modify source
- ✅ Distribute
- ✅ Private use

---

## 👤 Author

**Shlok Thorat**
- 📧 Email: shlok.thorat.cyb@ghrcem.raisoni.net
- 🐙 GitHub: [@shlok926](https://github.com/shlok926)
- 💼 LinkedIn: [shlok-thorat](https://linkedin.com)

---

## 📚 References

### Learning Resources
- [FFT Theory](https://en.wikipedia.org/wiki/Fast_Fourier_transform)
- [SciPy DSP](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [NumPy FFT](https://numpy.org/doc/stable/reference/fft.html)

### Related Tools
- [Audacity](https://www.audacityteam.org/) - Audio editing
- [GNU Octave](https://www.gnu.org/software/octave/) - MATLAB alternative
- [MATLAB](https://www.mathworks.com/) - Professional DSP

---

## 🎓 Academic Citation

If you use this tool in research, please cite:

```bibtex
@software{fft_analyzer_2026,
  title={FFT Signal Analyzer: Real-Time Signal Processing \& Analysis},
  author={Thorat, Shlok},
  year={2026},
  url={https://github.com/shlok926/fft-signal-analyzer}
}
```

---

## 🙏 Acknowledgments

Built with:
- 🙏 NumPy/SciPy/Pandas (DSP algorithms)
- 🙏 Streamlit (Web framework)
- 🙏 Plotly (Interactive plots)
- 🙏 Scikit-learn (ML algorithms)
- 🙏 All open-source contributors

---

## 📞 Support & Feedback

### Get Help
- 📖 [Documentation](QUICKSTART.md)
- 🐙 [GitHub Issues](https://github.com/shlok926/fft-signal-analyzer/issues)
- 💬 [Discussions](https://github.com/shlok926/fft-signal-analyzer/discussions)

### Share Feedback
- ⭐ Star the repository if you find it useful
- 🐛 Report bugs
- 💡 Suggest improvements
- 📢 Spread the word!

---

<div align="center">

### Made with ❤️  for signal processing enthusiasts

**[⬆ back to top](#-fft-signal-analyzer)**

</div>
