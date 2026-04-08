"""Digital filtering engine for FFT Signal Analyzer."""

import numpy as np
from scipy import signal as sp_signal

from ..models import SignalData
from ..utils import logger, validate_filter_params


class FilterEngine:
    """Apply digital filters to signals."""

    @staticmethod
    def low_pass(
        signal_data: SignalData,
        cutoff_hz: float,
        order: int = 4,
    ) -> SignalData:
        """Apply low-pass Butterworth filter.
        
        Args:
            signal_data: SignalData object to filter.
            cutoff_hz: Cutoff frequency in Hz.
            order: Filter order (default: 4).
            
        Returns:
            Filtered SignalData object.
        """
        # Validate filter parameters
        is_valid, cutoff_hz, warning = validate_filter_params(
            cutoff_hz, signal_data.fs, "lowpass"
        )
        if not is_valid:
            raise ValueError(warning)
        if warning:
            logger.warning(warning)

        # Normalize cutoff frequency
        nyquist = signal_data.fs / 2.0
        normalized_cutoff = cutoff_hz / nyquist

        # Design filter
        sos = sp_signal.butter(order, normalized_cutoff, btype='low', output='sos')

        # Apply zero-phase filter
        filtered = sp_signal.sosfiltfilt(sos, signal_data.amplitude)

        logger.info(
            f"Applied low-pass filter: cutoff={cutoff_hz} Hz, order={order}"
        )

        return SignalData(
            time=signal_data.time.copy(),
            amplitude=filtered,
            fs=signal_data.fs,
            label=f"{signal_data.label} (LP)",
            source=signal_data.source,
        )

    @staticmethod
    def high_pass(
        signal_data: SignalData,
        cutoff_hz: float,
        order: int = 4,
    ) -> SignalData:
        """Apply high-pass Butterworth filter.
        
        Args:
            signal_data: SignalData object to filter.
            cutoff_hz: Cutoff frequency in Hz.
            order: Filter order (default: 4).
            
        Returns:
            Filtered SignalData object.
        """
        # Validate filter parameters
        is_valid, cutoff_hz, warning = validate_filter_params(
            cutoff_hz, signal_data.fs, "highpass"
        )
        if not is_valid:
            raise ValueError(warning)
        if warning:
            logger.warning(warning)

        # Normalize cutoff frequency
        nyquist = signal_data.fs / 2.0
        normalized_cutoff = cutoff_hz / nyquist

        # Design filter
        sos = sp_signal.butter(order, normalized_cutoff, btype='high', output='sos')

        # Apply zero-phase filter
        filtered = sp_signal.sosfiltfilt(sos, signal_data.amplitude)

        logger.info(
            f"Applied high-pass filter: cutoff={cutoff_hz} Hz, order={order}"
        )

        return SignalData(
            time=signal_data.time.copy(),
            amplitude=filtered,
            fs=signal_data.fs,
            label=f"{signal_data.label} (HP)",
            source=signal_data.source,
        )

    @staticmethod
    def band_pass(
        signal_data: SignalData,
        low_cutoff_hz: float,
        high_cutoff_hz: float,
        order: int = 4,
    ) -> SignalData:
        """Apply band-pass Butterworth filter.
        
        Args:
            signal_data: SignalData object to filter.
            low_cutoff_hz: Lower cutoff frequency in Hz.
            high_cutoff_hz: Upper cutoff frequency in Hz.
            order: Filter order (default: 4).
            
        Returns:
            Filtered SignalData object.
        """
        # Validate filter parameters
        is_valid, low_cutoff_hz, warning = validate_filter_params(
            low_cutoff_hz, signal_data.fs, "bandpass"
        )
        if not is_valid:
            raise ValueError(warning)

        is_valid, high_cutoff_hz, warning2 = validate_filter_params(
            high_cutoff_hz, signal_data.fs, "bandpass"
        )
        if not is_valid:
            raise ValueError(warning2)

        if low_cutoff_hz >= high_cutoff_hz:
            raise ValueError(
                f"Low cutoff ({low_cutoff_hz}) must be < high cutoff ({high_cutoff_hz})"
            )

        # Normalize cutoff frequencies
        nyquist = signal_data.fs / 2.0
        normalized_low = low_cutoff_hz / nyquist
        normalized_high = high_cutoff_hz / nyquist

        # Design filter
        sos = sp_signal.butter(
            order,
            [normalized_low, normalized_high],
            btype='band',
            output='sos'
        )

        # Apply zero-phase filter
        filtered = sp_signal.sosfiltfilt(sos, signal_data.amplitude)

        logger.info(
            f"Applied band-pass filter: "
            f"[{low_cutoff_hz}, {high_cutoff_hz}] Hz, order={order}"
        )

        return SignalData(
            time=signal_data.time.copy(),
            amplitude=filtered,
            fs=signal_data.fs,
            label=f"{signal_data.label} (BP)",
            source=signal_data.source,
        )

    @staticmethod
    def notch(
        signal_data: SignalData,
        notch_freq_hz: float,
        quality_factor: float = 30.0,
    ) -> SignalData:
        """Apply notch filter to remove specific frequency.
        
        Args:
            signal_data: SignalData object to filter.
            notch_freq_hz: Frequency to notch in Hz.
            quality_factor: Quality factor Q (default: 30).
            
        Returns:
            Filtered SignalData object.
        """
        # Validate notch frequency
        if notch_freq_hz <= 0 or notch_freq_hz >= signal_data.fs / 2:
            raise ValueError(
                f"Notch frequency must be in (0, {signal_data.fs/2}) Hz"
            )

        # Design notch filter
        b, a = sp_signal.iirnotch(
            notch_freq_hz,
            quality_factor,
            fs=signal_data.fs
        )

        # Convert to SOS format for numerical stability
        sos = sp_signal.tf2sos(b, a)

        # Apply zero-phase filter
        filtered = sp_signal.sosfiltfilt(sos, signal_data.amplitude)

        logger.info(
            f"Applied notch filter: notch={notch_freq_hz} Hz, Q={quality_factor}"
        )

        return SignalData(
            time=signal_data.time.copy(),
            amplitude=filtered,
            fs=signal_data.fs,
            label=f"{signal_data.label} (Notch)",
            source=signal_data.source,
        )

    @staticmethod
    def get_frequency_response(
        filter_type: str,
        fs: float,
        cutoff_hz: float = None,
        low_cutoff_hz: float = None,
        high_cutoff_hz: float = None,
        order: int = 4,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Get frequency response of a filter.
        
        Args:
            filter_type: 'lowpass', 'highpass', 'bandpass', 'notch'.
            fs: Sampling frequency in Hz.
            cutoff_hz: Cutoff frequency (for LP/HP).
            low_cutoff_hz: Lower cutoff (for BP).
            high_cutoff_hz: Upper cutoff (for BP).
            order: Filter order.
            
        Returns:
            Tuple of (frequencies, magnitude_response).
        """
        nyquist = fs / 2.0

        if filter_type.lower() == 'lowpass':
            normalized = cutoff_hz / nyquist
            sos = sp_signal.butter(order, normalized, btype='low', output='sos')
        elif filter_type.lower() == 'highpass':
            normalized = cutoff_hz / nyquist
            sos = sp_signal.butter(order, normalized, btype='high', output='sos')
        elif filter_type.lower() == 'bandpass':
            norm_low = low_cutoff_hz / nyquist
            norm_high = high_cutoff_hz / nyquist
            sos = sp_signal.butter(
                order,
                [norm_low, norm_high],
                btype='band',
                output='sos'
            )
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")

        # Compute frequency response
        wd, h = sp_signal.sosfreqz(sos, worN=512)
        freqs = wd * fs / (2 * np.pi)

        return freqs, np.abs(h)
