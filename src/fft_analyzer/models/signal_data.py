"""Signal data model for time-domain signals."""

from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class SignalData:
    """Represents a time-domain signal.
    
    Attributes:
        time: Time axis in seconds (1D numpy array).
        amplitude: Signal amplitude values (1D numpy array).
        fs: Sampling frequency in Hz.
        label: Display name for the signal.
        source: Origin of the signal ('generated', 'csv', 'wav', 'npy').
    """

    time: np.ndarray
    amplitude: np.ndarray
    fs: float
    label: str
    source: Literal["generated", "csv", "wav", "npy"]

    def __post_init__(self) -> None:
        """Validate signal data after initialization."""
        if len(self.time) != len(self.amplitude):
            raise ValueError("Time and amplitude arrays must have same length")
        if self.fs <= 0:
            raise ValueError("Sampling frequency must be positive")
        if len(self.time) < 2:
            raise ValueError("Signal must have at least 2 samples")

    @property
    def duration(self) -> float:
        """Calculate signal duration in seconds."""
        return (len(self.amplitude) - 1) / self.fs

    @property
    def num_samples(self) -> int:
        """Get number of samples."""
        return len(self.amplitude)

    @property
    def nyquist_freq(self) -> float:
        """Get Nyquist frequency (fs/2)."""
        return self.fs / 2.0

    def remove_dc_offset(self) -> "SignalData":
        """Return a new SignalData with DC offset removed.
        
        Returns:
            New SignalData with mean-subtracted amplitude.
        """
        amplitude_centered = self.amplitude - np.mean(self.amplitude)
        return SignalData(
            time=self.time.copy(),
            amplitude=amplitude_centered,
            fs=self.fs,
            label=self.label,
            source=self.source,
        )

    def get_power(self) -> float:
        """Calculate signal power (RMS squared).
        
        Returns:
            Power in linear scale.
        """
        return float(np.mean(self.amplitude**2))
