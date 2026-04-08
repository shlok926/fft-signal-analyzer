"""Spectrum data model for frequency-domain representation."""

from dataclasses import dataclass

import numpy as np


@dataclass
class SpectrumData:
    """Represents a frequency-domain signal (FFT output).
    
    Attributes:
        freqs: Frequency bins in Hz (1D numpy array).
        magnitude: Linear magnitude spectrum (1D numpy array).
        magnitude_db: Magnitude spectrum in dB (1D numpy array).
        phase: Phase spectrum in radians (1D numpy array).
        psd: Power Spectral Density (1D numpy array).
        window: Window function applied before FFT.
        N: Original FFT length.
    """

    freqs: np.ndarray
    magnitude: np.ndarray
    magnitude_db: np.ndarray
    phase: np.ndarray
    psd: np.ndarray
    window: str
    N: int

    def __post_init__(self) -> None:
        """Validate spectrum data after initialization."""
        expected_len = len(self.freqs)
        if len(self.magnitude) != expected_len:
            raise ValueError("magnitude length must match freqs")
        if len(self.magnitude_db) != expected_len:
            raise ValueError("magnitude_db length must match freqs")
        if len(self.phase) != expected_len:
            raise ValueError("phase length must match freqs")
        if len(self.psd) != expected_len:
            raise ValueError("psd length must match freqs")
        if self.N < len(self.freqs):
            raise ValueError("N must be >= number of frequency bins")

    @property
    def num_bins(self) -> int:
        """Get number of frequency bins."""
        return len(self.freqs)

    @property
    def freq_resolution(self) -> float:
        """Get frequency resolution (Δf = fs/N).
        
        Note: fs is not stored directly; resolution is freqs[1] - freqs[0].
        """
        if len(self.freqs) > 1:
            return float(self.freqs[1] - self.freqs[0])
        return 0.0

    @property
    def max_magnitude(self) -> float:
        """Get maximum magnitude in linear scale."""
        return float(np.max(self.magnitude))

    @property
    def max_magnitude_db(self) -> float:
        """Get maximum magnitude in dB."""
        return float(np.max(self.magnitude_db))

    def get_bin_at_frequency(self, freq: float) -> int:
        """Find the bin index closest to a given frequency.
        
        Args:
            freq: Target frequency in Hz.
            
        Returns:
            Index of the closest frequency bin.
        """
        return int(np.argmin(np.abs(self.freqs - freq)))

    def get_magnitude_at_frequency(self, freq: float) -> tuple[float, float]:
        """Get magnitude (linear and dB) at a specific frequency.
        
        Args:
            freq: Target frequency in Hz.
            
        Returns:
            Tuple of (magnitude_linear, magnitude_db).
        """
        bin_idx = self.get_bin_at_frequency(freq)
        return float(self.magnitude[bin_idx]), float(self.magnitude_db[bin_idx])
