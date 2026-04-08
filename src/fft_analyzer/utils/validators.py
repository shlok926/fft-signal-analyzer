"""Input validation utilities."""

import os
from pathlib import Path
from typing import Optional

import numpy as np

from .logger import logger


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


def validate_signal_file(file_path: str) -> tuple[bool, str]:
    """Validate that a signal file exists and is accessible.
    
    Error Code: E001
    
    Args:
        file_path: Path to the signal file.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        p = Path(file_path)
        if not p.exists():
            msg = f"[E001] File not found: {file_path}"
            logger.error(msg)
            return False, msg

        if not p.is_file():
            msg = f"[E001] Path is not a file: {file_path}"
            logger.error(msg)
            return False, msg

        # Check file extension
        valid_extensions = {".csv", ".wav", ".npy"}
        if p.suffix.lower() not in valid_extensions:
            msg = (
                f"[E001] Unsupported file format: {p.suffix}. "
                f"Supported: {valid_extensions}"
            )
            logger.error(msg)
            return False, msg

        return True, ""

    except Exception as e:
        msg = f"[E001] Error validating file: {str(e)}"
        logger.error(msg)
        return False, msg


def validate_sampling_rate(fs: Optional[float]) -> tuple[bool, float, str]:
    """Validate sampling rate.
    
    Error Code: E003
    
    Args:
        fs: Sampling rate in Hz. If None, returns default 1000 Hz.
        
    Returns:
        Tuple of (is_valid, validated_fs, warning_message).
    """
    default_fs = 1000.0

    if fs is None:
        msg = "[E003] Sampling rate not provided. Defaulting to 1000 Hz."
        logger.warning(msg)
        return True, default_fs, msg

    if not isinstance(fs, (int, float)):
        msg = "[E003] Sampling rate must be a number."
        logger.error(msg)
        return False, default_fs, msg

    if fs <= 0:
        msg = "[E003] Sampling rate must be positive."
        logger.error(msg)
        return False, default_fs, msg

    if fs < 1.0:
        msg = "[E003] Sampling rate is very low. Recommended: >= 1 Hz."
        logger.warning(msg)

    return True, float(fs), ""


def validate_signal_length(num_samples: int) -> tuple[bool, str]:
    """Validate signal length.
    
    Error Code: E004
    
    Args:
        num_samples: Number of samples in the signal.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    min_samples = 4

    if not isinstance(num_samples, int):
        msg = "[E004] Number of samples must be an integer."
        logger.error(msg)
        return False, msg

    if num_samples < min_samples:
        msg = (
            f"[E004] Signal too short. Minimum {min_samples} samples required. "
            f"Got {num_samples}."
        )
        logger.error(msg)
        return False, msg

    return True, ""


def validate_filter_params(
    cutoff_freq: float, fs: float, filter_type: str = "lowpass"
) -> tuple[bool, float, str]:
    """Validate filter parameters.
    
    Error Code: E005
    
    Args:
        cutoff_freq: Filter cutoff frequency in Hz.
        fs: Sampling frequency in Hz.
        filter_type: Type of filter ('lowpass', 'highpass', 'bandpass', 'notch').
        
    Returns:
        Tuple of (is_valid, corrected_cutoff, warning_message).
    """
    nyquist = fs / 2.0

    if cutoff_freq <= 0:
        msg = "[E005] Cutoff frequency must be positive."
        logger.error(msg)
        return False, cutoff_freq, msg

    if cutoff_freq >= nyquist:
        corrected = nyquist - 1.0
        msg = (
            f"[E005] Cutoff frequency {cutoff_freq} Hz >= Nyquist {nyquist} Hz. "
            f"Clamped to {corrected} Hz."
        )
        logger.warning(msg)
        return True, corrected, msg

    return True, cutoff_freq, ""


def validate_signal_content(signal: list[float] | np.ndarray) -> tuple[bool, str]:
    """Validate signal content (check for all-zero).
    
    Error Code: E006
    
    Args:
        signal: Signal array/list.
        
    Returns:
        Tuple of (is_valid, warning_message).
    """
    import numpy as np

    arr = np.asarray(signal)

    if np.allclose(arr, 0):
        msg = "[E006] Warning: All-zero signal detected. No frequency content."
        logger.warning(msg)
        return True, msg

    if np.any(np.isnan(arr)):
        msg = "[E006] Error: Signal contains NaN values."
        logger.error(msg)
        return False, msg

    if np.any(np.isinf(arr)):
        msg = "[E006] Error: Signal contains infinite values."
        logger.error(msg)
        return False, msg

    return True, ""


# Helper for CSV validation
def validate_csv_format(file_path: str) -> tuple[bool, str]:
    """Validate CSV format (should have 1 or 2 columns).
    
    Error Code: E002
    
    Args:
        file_path: Path to CSV file.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        import pandas as pd

        df = pd.read_csv(file_path)

        if df.shape[1] not in [1, 2]:
            msg = (
                f"[E002] CSV should have 1 or 2 columns "
                f"([time, amplitude] or [amplitude]). Got {df.shape[1]}."
            )
            logger.error(msg)
            return False, msg

        return True, ""

    except Exception as e:
        msg = f"[E002] Invalid CSV format: {str(e)}"
        logger.error(msg)
        return False, msg


import numpy as np
