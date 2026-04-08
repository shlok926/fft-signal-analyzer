"""FFT Analyzer main package."""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "FFT-based signal analyzer for frequency component extraction"

from .core import (
    SignalGenerator,
    SignalLoader,
    FFTEngine,
    FilterEngine,
    PeakDetector,
)
from .models import SignalData, SpectrumData, PeakInfo
from .visualization import Visualizer
from .export import Exporter

__all__ = [
    "SignalGenerator",
    "SignalLoader",
    "FFTEngine",
    "FilterEngine",
    "PeakDetector",
    "SignalData",
    "SpectrumData",
    "PeakInfo",
    "Visualizer",
    "Exporter",
]
