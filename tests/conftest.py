"""Pytest configuration and fixtures for FFT Signal Analyzer tests."""

import numpy as np
import pytest
import time
from typing import Dict, List

from fft_analyzer.models import SignalData, SpectrumData, PeakInfo
from fft_analyzer.core import SignalGenerator, FFTEngine


class PerformanceProfiler:
    """Track and report performance metrics."""
    
    def __init__(self):
        self.measurements: Dict[str, List[float]] = {}
    
    def measure(self, func_name: str, duration_ms: float):
        """Record a measurement."""
        if func_name not in self.measurements:
            self.measurements[func_name] = []
        self.measurements[func_name].append(duration_ms)
    
    def get_stats(self, func_name: str):
        """Get statistics for a function."""
        if func_name not in self.measurements:
            return None
        
        durations = self.measurements[func_name]
        return {
            'count': len(durations),
            'min': min(durations),
            'max': max(durations),
            'avg': np.mean(durations),
            'std': np.std(durations),
            'total': sum(durations),
        }
    
    def get_all_stats(self):
        """Get statistics for all functions."""
        return {name: self.get_stats(name) for name in self.measurements}
    
    def print_report(self):
        """Print performance report."""
        print("\n=== Performance Report ===")
        for func_name, stats in self.get_all_stats().items():
            if stats:
                print(f"\n{func_name}:")
                print(f"  Count: {stats['count']}")
                print(f"  Min: {stats['min']:.2f}ms")
                print(f"  Max: {stats['max']:.2f}ms")
                print(f"  Avg: {stats['avg']:.2f}ms")
                print(f"  Std: {stats['std']:.2f}ms")
                print(f"  Total: {stats['total']:.2f}ms")


@pytest.fixture
def sample_sine_wave():
    """Generate a simple 50 Hz sine wave for testing.
    
    Returns:
        SignalData object with 50 Hz sine wave.
    """
    fs = 1000.0
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)

    return SignalData(
        time=t,
        amplitude=signal,
        fs=fs,
        label="Test 50Hz Sine",
        source="generated",
    )


@pytest.fixture
def sample_composite_signal():
    """Generate a composite signal with multiple frequencies.
    
    Returns:
        SignalData object with 50 Hz + 120 Hz components.
    """
    fs = 1000.0
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

    return SignalData(
        time=t,
        amplitude=signal,
        fs=fs,
        label="Test Composite",
        source="generated",
    )


@pytest.fixture
def sample_noisy_signal():
    """Generate a noisy signal (low SNR).
    
    Returns:
        SignalData object with noise.
    """
    fs = 1000.0
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)
    noise = np.random.normal(0, 0.3, len(signal))
    noisy_signal = signal + noise

    return SignalData(
        time=t,
        amplitude=noisy_signal,
        fs=fs,
        label="Test Noisy Signal",
        source="generated",
    )


@pytest.fixture
def sample_spectrum():
    """Compute FFT of sample composite signal.
    
    Returns:
        SpectrumData object.
    """
    components = [
        {"frequency": 50, "amplitude": 1.0, "phase": 0},
        {"frequency": 120, "amplitude": 0.5, "phase": 0},
    ]

    signal_data = SignalGenerator.generate_signal(
        components=components,
        fs=1000.0,
        duration=1.0,
        snr_db=100,  # No noise
        label="Test Spectrum",
    )

    spectrum = FFTEngine.compute_fft(signal_data, window_type="hann")
    return spectrum


@pytest.fixture
def sample_peaks():
    """Create sample PeakInfo objects.
    
    Returns:
        List of PeakInfo objects.
    """
    return [
        PeakInfo(
            frequency=50.0,
            magnitude=0.5,
            magnitude_db=20.0 * np.log10(0.5),
            prominence=0.1,
            index=50,
        ),
        PeakInfo(
            frequency=120.0,
            magnitude=0.25,
            magnitude_db=20.0 * np.log10(0.25),
            prominence=0.05,
            index=120,
        ),
    ]


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducibility."""
    np.random.seed(42)
    yield
    np.random.seed(None)


# Additional fixtures for test_utils compatibility

@pytest.fixture
def pure_sine():
    """Generate a pure sine wave for testing."""
    fs = 1000.0
    duration = 1.0
    frequency = 100.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    
    return SignalData(
        time=t,
        amplitude=signal,
        fs=fs,
        label=f"Test {frequency}Hz Sine",
        source="generated",
    )


@pytest.fixture
def multi_tone():
    """Generate a multi-tone signal for testing."""
    components = [
        {"frequency": 50, "amplitude": 1.0, "phase": 0},
        {"frequency": 120, "amplitude": 0.5, "phase": 0},
        {"frequency": 200, "amplitude": 0.3, "phase": 0},
    ]
    
    return SignalGenerator.generate_signal(
        components=components,
        fs=1000.0,
        duration=1.0,
        snr_db=100,
        label="Test Multi-Tone",
    )


@pytest.fixture
def chirp():
    """Generate a chirp signal (frequency sweep)."""
    fs = 1000.0
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Chirp from 50 Hz to 500 Hz
    f0 = 50
    f1 = 500
    chirp_signal = np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * duration)))
    
    return SignalData(
        time=t,
        amplitude=chirp_signal,
        fs=fs,
        label="Test Chirp (50-500Hz)",
        source="generated",
    )


@pytest.fixture
def noisy_signal():
    """Generate a noisy signal."""
    fs = 1000.0
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 100 * t)
    
    # SNR = 20 dB
    signal_power = np.mean(signal**2)
    snr = 10**(20 / 10)
    noise_power = signal_power / snr
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    
    return SignalData(
        time=t,
        amplitude=signal + noise,
        fs=fs,
        label="Test Noisy Signal",
        source="generated",
    )


@pytest.fixture
def profiler():
    """Create a performance profiler for tests."""
    return PerformanceProfiler()

