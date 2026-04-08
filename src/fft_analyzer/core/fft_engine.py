"""FFT computation engine for signal analysis."""

import numpy as np
from scipy import signal as sp_signal

from ..models import SignalData, SpectrumData
from ..utils import logger, math_utils


class FFTEngine:
    """Perform FFT and spectral analysis on signals."""

    @staticmethod
    def apply_window(signal_data: np.ndarray, window_type: str = "hann") -> np.ndarray:
        """Apply a window function to a signal.
        
        Args:
            signal_data: Input signal array.
            window_type: Type of window ('hann', 'hamming', 'blackman', 'rectangle').
            
        Returns:
            Windowed signal array.
        """
        return math_utils.apply_window(signal_data, window_type)

    @staticmethod
    def compute_fft(
        signal_data: SignalData,
        window_type: str = "hann",
        zero_pad: bool = True,
    ) -> SpectrumData:
        """Compute FFT of a signal and return spectrum data.
        
        Args:
            signal_data: SignalData object.
            window_type: Window function to apply ('hann', 'hamming', 'blackman', 'rectangle').
            zero_pad: Whether to zero-pad to next power of 2.
            
        Returns:
            SpectrumData object with frequency, magnitude, phase, and power info.
        """
        # Get signal and remove DC offset
        x = signal_data.amplitude - np.mean(signal_data.amplitude)
        fs = signal_data.fs

        # Apply window
        x_windowed = FFTEngine.apply_window(x, window_type)
        logger.debug(f"Applied {window_type} window")

        # Determine FFT length
        N_orig = len(x_windowed)
        if zero_pad:
            N = math_utils.next_power_of_2(N_orig)
            x_windowed = np.pad(x_windowed, (0, N - N_orig), mode="constant")
            logger.debug(f"Zero-padded: {N_orig} → {N}")
        else:
            N = N_orig

        # Compute FFT
        X = np.fft.fft(x_windowed)

        # Convert to one-sided spectrum
        magnitude = np.abs(X[:N//2 + 1])
        # Account for one-sided spectrum (except DC and Nyquist)
        magnitude[1:-1] *= 2.0 / N_orig
        magnitude[0] /= N_orig  # DC component
        magnitude[-1] /= N_orig  # Nyquist (if present)

        # Compute dB magnitude
        magnitude_db = np.array([math_utils.linear_to_db(m) for m in magnitude])

        # Compute phase
        phase = np.angle(X[:N//2 + 1])

        # Frequency axis
        freqs = np.fft.fftfreq(N, 1/fs)[:N//2 + 1]

        # Compute Power Spectral Density (Welch method)
        # Convert 'rectangle' to 'boxcar' for scipy compatibility
        scipy_window = 'boxcar' if window_type.lower() == 'rectangle' else window_type
        freqs_psd, psd = sp_signal.welch(
            signal_data.amplitude,
            fs=fs,
            window=scipy_window,
            nperseg=min(256, len(signal_data.amplitude)),
            scaling='density'
        )

        logger.info(
            f"FFT computed: {N} points, Δf={freqs[1]-freqs[0]:.2f} Hz, "
            f"max_freq={freqs[-1]:.2f} Hz"
        )

        return SpectrumData(
            freqs=freqs,
            magnitude=magnitude,
            magnitude_db=magnitude_db,
            phase=phase,
            psd=psd if len(psd) == len(freqs) else np.interp(freqs, freqs_psd, psd),
            window=window_type,
            N=N,
        )

    @staticmethod
    def compute_psd(
        signal_data: SignalData,
        window_type: str = "hann",
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute Power Spectral Density using Welch method.
        
        Args:
            signal_data: SignalData object.
            window_type: Window function to use.
            
        Returns:
            Tuple of (frequencies, power_spectral_density).
        """
        # Convert 'rectangle' to 'boxcar' for scipy compatibility
        scipy_window = 'boxcar' if window_type.lower() == 'rectangle' else window_type
        freqs, psd = sp_signal.welch(
            signal_data.amplitude,
            fs=signal_data.fs,
            window=scipy_window,
            nperseg=min(256, len(signal_data.amplitude)),
            scaling='density'
        )

        logger.debug(f"PSD computed: {len(freqs)} bins")

        return freqs, psd

    @staticmethod
    def to_db(magnitude: np.ndarray) -> np.ndarray:
        """Convert magnitude spectrum to dB scale.
        
        Args:
            magnitude: Linear magnitude array.
            
        Returns:
            Magnitude in dB.
        """
        return np.array([math_utils.linear_to_db(m) for m in magnitude])

    @staticmethod
    def inverse_fft(
        magnitude: np.ndarray,
        phase: np.ndarray,
        n_samples: int,
    ) -> np.ndarray:
        """Reconstruct time-domain signal from spectrum.
        
        Args:
            magnitude: One-sided magnitude spectrum.
            phase: One-sided phase spectrum.
            n_samples: Desired number of samples in output.
            
        Returns:
            Reconstructed signal in time domain.
        """
        # Reconstruct complex spectrum
        X = magnitude * np.exp(1j * phase)

        # Mirror for negative frequencies (one-sided to two-sided)
        X_full = np.concatenate([X, np.conj(X[-2:0:-1])])

        # IFFT
        x = np.fft.ifft(X_full).real

        # Trim to original length
        return x[:n_samples]
