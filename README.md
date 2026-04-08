# FFT Signal Analyzer

A comprehensive Desktop/Web application for Fast Fourier Transform (FFT)-based signal analysis, frequency component extraction, and signal processing.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

The **FFT Signal Analyzer** is a Python-based tool designed for:
- **Signal Generation**: Create synthetic signals with configurable frequency components and noise
- **Spectral Analysis**: Compute FFT with various windowing functions and zero-padding
- **Noise Filtering**: Apply low-pass, high-pass, band-pass, and notch filters
- **Peak Detection**: Automatically identify dominant frequency components
- **Interactive Visualization**: Explore time-domain, frequency-domain, phase, and power spectral density plots
- **Export**: Save results to CSV, PNG/SVG plots, and PDF reports

### Target Users
- RF Engineers & Signal Processing Researchers
- DSP Students & Educators
- Embedded Systems Developers
- Anyone working with frequency analysis

## Features

✨ **Core Features**
- ✅ Composite signal generation (multiple sinusoids + noise)
- ✅ FFT computation with Hann/Hamming/Blackman/Rectangle windows
- ✅ Zero-padding for improved frequency resolution
- ✅ Butterworth filters (LP/HP/BP/Notch) with zero-phase response
- ✅ Automatic peak detection with prominence thresholds
- ✅ Harmonic series analysis & THD calculation
- ✅ Interactive Plotly dashboard
- ✅ Command-line interface (CLI)
- ✅ CSV/WAV/NPY file import
- ✅ Export to PNG/SVG/PDF/CSV

📊 **Visualization**
- Time-domain amplitude plot
- Frequency spectrum (dB & linear scales)
- Phase spectrum (wrapped & unwrapped)
- Power Spectral Density (Welch method)
- Detected peaks with annotations
- Before/after filter comparison plots

## Installation

### Prerequisites
- Python 3.11 or higher
- pip or Poetry

### Quick Start (with Poetry)

```bash
# Clone repository
git clone https://github.com/yourusername/fft-signal-analyzer.git
cd fft-signal-analyzer

# Install all dependencies
make dev-setup

# Run dashboard
make run
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python -m fft_analyzer.ui.app
```

## Usage

### 1. Interactive Dashboard

Launch the web-based dashboard:

```bash
make run
# or
poetry run fft-dashboard
```

Then open your browser to `http://127.0.0.1:8050`

**Dashboard Features:**
- Configure signal parameters (frequencies, amplitudes, SNR)
- Select window function and filter type
- View real-time plots after clicking "Analyze"
- Inspect detected peaks in a table
- Export analysis results

### 2. Command-Line Interface

Generate and analyze signals:

```bash
# Generate a test signal
fft-analyzer generate --freq 50 120 --amp 1.0 0.5 --snr 20 --fs 1000 --duration 1.0 --output signal.csv

# Analyze a signal file
fft-analyzer analyze --input signal.csv --window hann --fs 1000 --output-dir outputs

# Create interactive plot
fft-analyzer plot --input outputs/spectrum.csv --output output/plot.html

# Launch dashboard
fft-analyzer dashboard --port 8050 --debug
```

### 3. Python API

Use as a library:

```python
from fft_analyzer import SignalGenerator, FFTEngine, PeakDetector, Visualizer

# Generate signal
signal = SignalGenerator.generate_signal(
    components=[
        {"frequency": 50, "amplitude": 1.0, "phase": 0},
        {"frequency": 120, "amplitude": 0.5, "phase": 0},
    ],
    fs=1000,
    duration=1.0,
    snr_db=20,
    label="My Signal",
)

# Compute FFT
spectrum = FFTEngine.compute_fft(signal, window_type="hann", zero_pad=True)

# Detect peaks
peaks = PeakDetector.detect_peaks(spectrum)

# Create plots
fig_freq = Visualizer.plot_frequency_domain(spectrum, peaks)
fig_phase = Visualizer.plot_phase_spectrum(spectrum)

fig_freq.show()
```

## Project Structure

```
fft_signal_analyzer/
├── src/fft_analyzer/           # Main package
│   ├── core/                   # DSP algorithms
│   │   ├── signal_generator.py
│   │   ├── signal_loader.py
│   │   ├── fft_engine.py
│   │   ├── filter_engine.py
│   │   └── peak_detector.py
│   ├── models/                 # Data classes
│   ├── ui/                     # Dash dashboard
│   ├── visualization/          # Plotly plots
│   ├── export/                 # CSV/PNG/PDF export
│   ├── cli/                    # Click CLI
│   └── utils/                  # Helpers
├── tests/                      # Unit & integration tests
├── config/                     # Configuration files
├── notebooks/                  # Jupyter notebooks
├── outputs/                    # Results directory (git-ignored)
├── pyproject.toml             # Poetry dependencies
├── Makefile                   # Development commands
└── README.md                  # This file
```

## Development

### Setup Development Environment

```bash
make dev-setup
```

This installs all dependencies and sets up pre-commit hooks.

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
pytest tests/unit/test_fft_engine.py -v
```

### Code Quality

```bash
# Lint code
make lint

# Format code (black + ruff auto-fix)
make format

# Type checking
poetry run mypy src/fft_analyzer
```

### Performance Benchmarks

```bash
make benchmark
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

## Configuration

Edit `config/config.yaml` to customize default parameters:

```yaml
signal:
  sampling_rate: 1000
  duration: 1.0
  components:
    - frequency: 50
      amplitude: 1.0
      phase: 0.0
  noise:
    enabled: true
    snr_db: 20

fft:
  window: "hann"
  zero_padding: true

filter:
  type: "lowpass"
  cutoff_hz: 200
  order: 4

peaks:
  prominence_factor: 0.1
  min_distance_hz: 5
```

## Technical Details

### FFT Algorithm
- **Method**: Cooley-Tukey Radix-2 DIT FFT via NumPy
- **Windowing**: Hann, Hamming, Blackman, Rectangle
- **Zero-Padding**: Automatic to next power of 2
- **Spectrum**: One-sided, normalized by FFT length

### Filtering
- **Algorithm**: Butterworth IIR (via SciPy)
- **Zero-Phase**: sosfiltfilt for symmetry
- **Types**: Low-Pass, High-Pass, Band-Pass, Notch

### Peak Detection
- **Algorithm**: scipy.signal.find_peaks()
- **Criteria**: Height threshold + prominence
- **Output**: Frequency, magnitude (linear + dB), prominence

## Troubleshooting

### Issue: Dash app won't start
**Solution**: Ensure ports 8050 is not in use, or specify a different port:
```bash
fft-analyzer dashboard --port 8051
```

### Issue: ImportError for scipy/plotly
**Solution**: Reinstall dependencies:
```bash
make install-dev
```

### Issue: FFT results don't look right
**Check**: 
- Sample rate is correct (Nyquist = fs/2)
- Signal has enough samples (≥ 4)
- Window function is appropriate for your signal

## Performance

Typical performance on modern hardware:
- 1,024 point FFT: < 1 ms
- 65,536 point FFT: < 10 ms
- 1,048,576 point FFT: < 500 ms
- 10,000,000 point FFT: < 5 seconds

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## Testing

All changes must pass:
```bash
make test && make lint
```

## License

MIT License - see LICENSE file for details

## Author

**Your Name** - [GitHub Profile](https://github.com/yourusername)

## Acknowledgments

- NumPy/SciPy for core DSP algorithms
- Plotly for interactive visualizations
- Dash for web framework
- All contributors and testers

## Citation

If you use this project in research, please cite:

```bibtex
@software{fft_analyzer_2026,
  title={FFT Signal Analyzer: Fast Fourier Transform-based Signal Analysis Tool},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/fft-signal-analyzer}
}
```

## Support

For issues, questions, or suggestions:
- 📝 Open an issue on GitHub
- 💬 Discussions/Q&A on GitHub
- 📧 Email: your.email@example.com

---

**Made with ❤️ for signal processing enthusiasts**
