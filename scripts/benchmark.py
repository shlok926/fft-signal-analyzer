"""Performance benchmarking script for FFT Signal Analyzer."""

import time

import numpy as np

from fft_analyzer.core import SignalGenerator, FFTEngine
from fft_analyzer.utils import logger


def benchmark_fft_generation():
    """Benchmark FFT computation on various signal sizes."""
    logger.info("=" * 60)
    logger.info("FFT Performance Benchmark")
    logger.info("=" * 60)

    sizes = [1024, 65536, 1048576, 10485760]

    for size in sizes:
        try:
            # Generate random signal
            t = np.linspace(0, 1.0, size)
            freq = 50
            signal = np.sin(2 * np.pi * freq * t)

            from fft_analyzer.models import SignalData

            signal_data = SignalData(
                time=t,
                amplitude=signal,
                fs=1000,
                label=f"Benchmark {size}",
                source="generated",
            )

            # Time FFT
            start = time.perf_counter()
            spectrum = FFTEngine.compute_fft(signal_data, window_type="hann", zero_pad=True)
            elapsed = time.perf_counter() - start

            throughput = size / elapsed / 1e6  # Mega-samples per second
            logger.info(
                f"  {size:>10} samples: {elapsed*1000:>8.2f} ms "
                f"({throughput:>6.2f} Msamples/s)"
            )

        except Exception as e:
            logger.error(f"  {size:>10} samples: FAILED - {str(e)}")

    logger.info("=" * 60)


def benchmark_signal_generation():
    """Benchmark synthetic signal generation."""
    logger.info("Signal Generation Benchmark")
    logger.info("=" * 60)

    components = [
        {"frequency": 50, "amplitude": 1.0, "phase": 0},
        {"frequency": 120, "amplitude": 0.5, "phase": 0},
        {"frequency": 250, "amplitude": 0.3, "phase": 0},
    ]

    durations = [0.1, 1.0, 10.0]
    fs = 10000

    for duration in durations:
        try:
            start = time.perf_counter()
            signal = SignalGenerator.generate_signal(
                components=components,
                fs=fs,
                duration=duration,
                snr_db=20,
            )
            elapsed = time.perf_counter() - start

            samples = len(signal.amplitude)
            throughput = samples / elapsed / 1e6

            logger.info(
                f"  Duration {duration}s ({samples:>10} samples): "
                f"{elapsed*1000:>8.2f} ms ({throughput:>6.2f} Msamples/s)"
            )

        except Exception as e:
            logger.error(f"  Duration {duration}s: FAILED - {str(e)}")

    logger.info("=" * 60)


if __name__ == "__main__":
    logger.info("Starting performance benchmarks...")
    logger.info("")

    benchmark_signal_generation()
    logger.info("")
    benchmark_fft_generation()

    logger.info("")
    logger.info("Benchmark complete!")
