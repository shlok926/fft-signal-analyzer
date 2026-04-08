"""Peak detection in frequency spectra."""

from typing import List

import numpy as np
from scipy import signal as sp_signal

from ..models import SpectrumData, PeakInfo
from ..utils import logger


class PeakDetector:
    """Detect and analyze peaks in frequency spectra."""

    @staticmethod
    def detect_peaks(
        spectrum_data: SpectrumData,
        height_threshold: float = 0.05,
        prominence_factor: float = 0.1,
        min_distance_hz: float = 5.0,
    ) -> List[PeakInfo]:
        """Detect dominant peaks in frequency spectrum.
        
        Uses scipy.signal.find_peaks() with prominence and height criteria.
        
        Args:
            spectrum_data: SpectrumData object.
            height_threshold: Minimum height threshold (fraction of max magnitude).
            prominence_factor: Minimum prominence (fraction of max magnitude).
            min_distance_hz: Minimum distance between peaks in Hz.
            
        Returns:
            List of PeakInfo objects, sorted by magnitude (descending).
        """
        magnitude = spectrum_data.magnitude
        freqs = spectrum_data.freqs

        # Compute thresholds
        max_magnitude = np.max(magnitude)
        height_min = height_threshold * max_magnitude
        prominence_min = prominence_factor * max_magnitude

        # Convert min distance from Hz to samples
        if len(freqs) > 1:
            freq_res = freqs[1] - freqs[0]
            min_dist_samples = max(1, int(min_distance_hz / freq_res))
        else:
            min_dist_samples = 1

        # Find peaks
        peak_indices, properties = sp_signal.find_peaks(
            magnitude,
            height=height_min,
            prominence=prominence_min,
            distance=min_dist_samples,
        )

        # Create PeakInfo objects
        peaks = []
        for idx in peak_indices:
            freq = float(freqs[idx])
            mag = float(magnitude[idx])
            mag_db = float(spectrum_data.magnitude_db[idx])
            prominence = float(properties['prominences'][list(peak_indices).index(idx)])

            peaks.append(
                PeakInfo(
                    frequency=freq,
                    magnitude=mag,
                    magnitude_db=mag_db,
                    prominence=prominence,
                    index=idx,
                )
            )

        # Sort by magnitude (descending)
        peaks.sort(reverse=True)

        logger.info(
            f"Detected {len(peaks)} peaks. "
            f"Threshold: {height_min:.4f}, Prominence: {prominence_min:.4f}"
        )

        return peaks

    @staticmethod
    def rank_by_magnitude(peaks: List[PeakInfo]) -> List[PeakInfo]:
        """Sort peaks by magnitude in descending order.
        
        Args:
            peaks: List of PeakInfo objects.
            
        Returns:
            Sorted list of PeakInfo objects.
        """
        return sorted(peaks, key=lambda p: p.magnitude, reverse=True)

    @staticmethod
    def rank_by_frequency(peaks: List[PeakInfo]) -> List[PeakInfo]:
        """Sort peaks by frequency in ascending order.
        
        Args:
            peaks: List of PeakInfo objects.
            
        Returns:
            Sorted list of PeakInfo objects.
        """
        return sorted(peaks, key=lambda p: p.frequency)

    @staticmethod
    def filter_peaks_by_snr(
        peaks: List[PeakInfo],
        min_snr_db: float = 3.0,
    ) -> List[PeakInfo]:
        """Filter peaks by signal-to-noise ratio (dB).
        
        Keeps only peaks with magnitude_db > min_snr_db.
        
        Args:
            peaks: List of PeakInfo objects.
            min_snr_db: Minimum SNR threshold in dB.
            
        Returns:
            Filtered list of PeakInfo objects.
        """
        if not peaks:
            return []

        noise_floor_db = min(p.magnitude_db for p in peaks)
        filtered = [
            p for p in peaks
            if (p.magnitude_db - noise_floor_db) >= min_snr_db
        ]

        logger.debug(f"Filtered peaks by SNR: {len(peaks)} → {len(filtered)}")

        return filtered

    @staticmethod
    def format_annotations(peaks: List[PeakInfo]) -> List[dict]:
        """Format peaks as annotation dictionaries for plotting.
        
        Args:
            peaks: List of PeakInfo objects.
            
        Returns:
            List of dictionaries with annotation info.
        """
        annotations = []

        for i, peak in enumerate(peaks, 1):
            annotations.append({
                "rank": i,
                "frequency_hz": peak.frequency,
                "magnitude_linear": peak.magnitude,
                "magnitude_db": peak.magnitude_db,
                "prominence": peak.prominence,
                "index": peak.index,
                "text": f"f={peak.frequency:.1f}Hz\n"
                        f"A={peak.magnitude:.4f}\n"
                        f"{peak.magnitude_db:.1f}dB",
            })

        return annotations

    @staticmethod
    def get_harmonic_series(
        fundamental_freq: float,
        peaks: List[PeakInfo],
        freq_tolerance_hz: float = 5.0,
        num_harmonics: int = 10,
    ) -> List[dict]:
        """Identify harmonics of a fundamental frequency.
        
        Args:
            fundamental_freq: Fundamental frequency in Hz.
            peaks: List of detected peaks.
            freq_tolerance_hz: Tolerance in frequency matching (Hz).
            num_harmonics: Maximum number of harmonics to find.
            
        Returns:
            List of harmonics with peak info.
        """
        harmonics = []

        for n in range(1, num_harmonics + 1):
            target_freq = n * fundamental_freq

            # Find closest peak
            closest_peak = None
            min_error = freq_tolerance_hz

            for peak in peaks:
                error = abs(peak.frequency - target_freq)
                if error < min_error:
                    min_error = error
                    closest_peak = peak

            if closest_peak:
                harmonics.append({
                    "harmonic_number": n,
                    "target_frequency_hz": target_freq,
                    "detected_frequency_hz": closest_peak.frequency,
                    "frequency_error_hz": closest_peak.frequency - target_freq,
                    "magnitude": closest_peak.magnitude,
                    "magnitude_db": closest_peak.magnitude_db,
                })

        logger.info(f"Identified {len(harmonics)} harmonics of {fundamental_freq} Hz")

        return harmonics

    @staticmethod
    def calculate_thd(
        fundamental_peak: PeakInfo,
        harmonic_peaks: List[PeakInfo],
    ) -> float:
        """Calculate Total Harmonic Distortion (THD).
        
        THD = sqrt(sum(A_n^2 for n=2..N)) / A_1
        
        Args:
            fundamental_peak: PeakInfo of fundamental frequency.
            harmonic_peaks: List of PeakInfo objects for harmonics (n >= 2).
            
        Returns:
            THD as a percentage.
        """
        if fundamental_peak.magnitude <= 0:
            return 0.0

        harmonic_rms = np.sqrt(np.sum([p.magnitude**2 for p in harmonic_peaks]))
        thd = (harmonic_rms / fundamental_peak.magnitude) * 100.0

        return float(thd)
