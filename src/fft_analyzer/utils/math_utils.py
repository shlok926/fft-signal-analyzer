"""Mathematical utilities for signal processing."""

import numpy as np


def snr_to_noise_std(signal_power: float, snr_db: float) -> float:
    """Convert SNR in dB to noise standard deviation.
    
    Formula: σ = sqrt(P_signal / 10^(SNR_dB/10))
    
    Args:
        signal_power: Signal power (RMS squared).
        snr_db: Signal-to-noise ratio in dB.
        
    Returns:
        Noise standard deviation.
    """
    if snr_db < 0:
        raise ValueError("SNR must be non-negative")
    if signal_power <= 0:
        raise ValueError("Signal power must be positive")

    snr_linear = 10 ** (snr_db / 10.0)
    noise_power = signal_power / snr_linear
    return float(np.sqrt(noise_power))


def linear_to_db(magnitude: float) -> float:
    """Convert linear magnitude to dB scale.
    
    Formula: 20 * log10(magnitude)
    
    Args:
        magnitude: Linear magnitude value.
        
    Returns:
        Magnitude in dB.
    """
    if magnitude <= 0:
        return -np.inf
    return float(20.0 * np.log10(magnitude))


def db_to_linear(magnitude_db: float) -> float:
    """Convert magnitude from dB to linear scale.
    
    Formula: 10^(magnitude_dB / 20)
    
    Args:
        magnitude_db: Magnitude in dB.
        
    Returns:
        Linear magnitude.
    """
    return float(10.0 ** (magnitude_db / 20.0))


def calculate_snr(signal: np.ndarray, noise: np.ndarray) -> float:
    """Calculate SNR between signal and noise.
    
    Args:
        signal: Signal array.
        noise: Noise array (same length as signal).
        
    Returns:
        SNR in dB.
    """
    if len(signal) != len(noise):
        raise ValueError("Signal and noise must have same length")

    signal_power = float(np.mean(signal**2))
    noise_power = float(np.mean(noise**2))

    if noise_power <= 0:
        return 100.0  # Arbitrary large value

    snr_linear = signal_power / noise_power
    return float(10.0 * np.log10(snr_linear))


def next_power_of_2(n: int) -> int:
    """Find the next power of 2 greater than or equal to n.
    
    Args:
        n: Input integer.
        
    Returns:
        Smallest power of 2 >= n.
    """
    if n <= 0:
        raise ValueError("Input must be positive")

    return int(2 ** np.ceil(np.log2(n)))


def apply_window(
    signal: np.ndarray, window_type: str = "hann"
) -> np.ndarray:
    """Apply a window function to a signal.
    
    Args:
        signal: Input signal array.
        window_type: Type of window ('hann', 'hamming', 'blackman', 'rectangle').
        
    Returns:
        Windowed signal.
        
    Raises:
        ValueError: If window_type is not supported.
    """
    N = len(signal)

    if window_type.lower() == "hann":
        window = np.hanning(N)
    elif window_type.lower() == "hamming":
        window = np.hamming(N)
    elif window_type.lower() == "blackman":
        window = np.blackman(N)
    elif window_type.lower() == "rectangle":
        window = np.ones(N)
    else:
        raise ValueError(
            f"Unknown window type: {window_type}. "
            "Supported: hann, hamming, blackman, rectangle"
        )

    return signal * window
