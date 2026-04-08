"""Signal generation for FFT Signal Analyzer."""

from typing import List

import numpy as np

from ..models import SignalData
from ..utils import snr_to_noise_std


class SignalGenerator:
    """Generate synthetic test signals."""

    @staticmethod
    def get_time_axis(duration: float, fs: float) -> np.ndarray:
        """Generate time axis.
        
        Args:
            duration: Signal duration in seconds.
            fs: Sampling frequency in Hz.
            
        Returns:
            Time axis array in seconds.
        """
        if duration <= 0:
            raise ValueError("Duration must be positive")
        if fs <= 0:
            raise ValueError("Sampling frequency must be positive")

        num_samples = int(duration * fs)
        return np.linspace(0, duration - 1 / fs, num_samples)

    @staticmethod
    def generate_sine(
        freq: float, amp: float, phase: float, t: np.ndarray
    ) -> np.ndarray:
        """Generate a sinusoidal component.
        
        Formula: A * sin(2π * f * t + φ)
        
        Args:
            freq: Frequency in Hz.
            amp: Amplitude.
            phase: Initial phase in radians.
            t: Time axis array.
            
        Returns:
            Sinusoidal signal array.
        """
        if freq < 0:
            raise ValueError("Frequency must be non-negative")
        if amp < 0:
            raise ValueError("Amplitude must be non-negative")

        return amp * np.sin(2 * np.pi * freq * t + phase)

    @staticmethod
    def compose_signal(
        components: list[dict],
        t: np.ndarray,
    ) -> np.ndarray:
        """Compose a signal from multiple frequency components.
        
        Each component dict should have: 'frequency', 'amplitude', 'phase'.
        
        Args:
            components: List of component dictionaries.
            t: Time axis array.
            
        Returns:
            Composite signal array.
        """
        if not components:
            raise ValueError("At least one component required")

        signal = np.zeros_like(t)

        for component in components:
            freq = component.get("frequency", 0)
            amp = component.get("amplitude", 1.0)
            phase = component.get("phase", 0)

            signal += SignalGenerator.generate_sine(freq, amp, phase, t)

        return signal

    @staticmethod
    def add_noise(
        signal: np.ndarray,
        snr_db: float,
    ) -> np.ndarray:
        """Add Gaussian white noise to a signal.
        
        Args:
            signal: Input signal array.
            snr_db: Signal-to-noise ratio in dB.
            
        Returns:
            Noisy signal array.
        """
        if snr_db < 0:
            raise ValueError("SNR must be non-negative")

        signal_power = float(np.mean(signal**2))
        noise_std = snr_to_noise_std(signal_power, snr_db)
        noise = np.random.normal(0, noise_std, len(signal))

        return signal + noise

    @staticmethod
    def generate_signal(
        components: list[dict],
        fs: float,
        duration: float,
        snr_db: float = 100,  # Default: very high SNR (essentially no noise)
        label: str = "Generated Signal",
    ) -> SignalData:
        """Generate a complete synthetic signal.
        
        Args:
            components: List of component dictionaries with 'frequency',
                        'amplitude', 'phase'.
            fs: Sampling frequency in Hz.
            duration: Signal duration in seconds.
            snr_db: Signal-to-noise ratio in dB (default: very high).
            label: Display name for the signal.
            
        Returns:
            SignalData object.
        """
        # Generate time axis
        t = SignalGenerator.get_time_axis(duration, fs)

        # Compose signal from components
        signal = SignalGenerator.compose_signal(components, t)

        # Add noise if SNR is specified
        if snr_db < 100:
            signal = SignalGenerator.add_noise(signal, snr_db)

        return SignalData(
            time=t,
            amplitude=signal,
            fs=fs,
            label=label,
            source="generated",
        )
