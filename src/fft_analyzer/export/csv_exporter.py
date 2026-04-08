"""CSV export functionality."""

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from ..models import SpectrumData, PeakInfo
from ..utils import logger


class CSVExporter:
    """Export spectrum data to CSV format."""

    @staticmethod
    def export_spectrum(
        spectrum_data: SpectrumData,
        output_path: str,
        peaks: List[PeakInfo] = None,
    ) -> None:
        """Export frequency spectrum to CSV.
        
        Args:
            spectrum_data: SpectrumData object.
            output_path: Path to output CSV file.
            peaks: Optional list of PeakInfo objects to include.
        """
        try:
            # Create dataframe
            data = {
                'Frequency_Hz': spectrum_data.freqs,
                'Magnitude_Linear': spectrum_data.magnitude,
                'Magnitude_dB': spectrum_data.magnitude_db,
                'Phase_Radians': spectrum_data.phase,
                'PSD': spectrum_data.psd,
            }

            df = pd.DataFrame(data)

            # Save to CSV
            df.to_csv(output_path, index=False)

            logger.info(f"Spectrum exported to CSV: {output_path}")

            # Export peaks if provided
            if peaks:
                peaks_path = str(Path(output_path).with_stem(
                    f"{Path(output_path).stem}_peaks"
                ))
                CSVExporter.export_peaks(peaks, peaks_path)

        except Exception as e:
            logger.error(f"Error exporting spectrum to CSV: {str(e)}")
            raise

    @staticmethod
    def export_peaks(
        peaks: List[PeakInfo],
        output_path: str,
    ) -> None:
        """Export detected peaks to CSV.
        
        Args:
            peaks: List of PeakInfo objects.
            output_path: Path to output CSV file.
        """
        try:
            data = {
                'Rank': [i + 1 for i in range(len(peaks))],
                'Frequency_Hz': [p.frequency for p in peaks],
                'Magnitude_Linear': [p.magnitude for p in peaks],
                'Magnitude_dB': [p.magnitude_db for p in peaks],
                'Prominence': [p.prominence for p in peaks],
                'Index': [p.index for p in peaks],
            }

            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)

            logger.info(f"Peaks exported to CSV: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting peaks to CSV: {str(e)}")
            raise

    @staticmethod
    def export_time_series(
        time: np.ndarray,
        amplitude: np.ndarray,
        output_path: str,
        label: str = "amplitude",
    ) -> None:
        """Export time-series data to CSV.
        
        Args:
            time: Time axis array.
            amplitude: Signal amplitude array.
            output_path: Path to output CSV file.
            label: Column label for amplitude.
        """
        try:
            data = {
                'Time_s': time,
                label: amplitude,
            }

            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)

            logger.info(f"Time series exported to CSV: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting time series to CSV: {str(e)}")
            raise
