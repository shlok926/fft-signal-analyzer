"""PDF export functionality for analysis reports."""

from pathlib import Path
from typing import List, Optional

import numpy as np
from fpdf import FPDF

from ..models import SpectrumData, PeakInfo, SignalData
from ..utils import logger


class PDFExporter:
    """Export analysis reports to PDF."""

    @staticmethod
    def create_report(
        output_path: str,
        title: str = "FFT Signal Analysis Report",
        signal_data: Optional[SignalData] = None,
        spectrum_data: Optional[SpectrumData] = None,
        peaks: Optional[List[PeakInfo]] = None,
        image_paths: Optional[List[str]] = None,
    ) -> None:
        """Create a comprehensive analysis report in PDF.
        
        Args:
            output_path: Path to output PDF file.
            title: Report title.
            signal_data: Optional SignalData object.
            spectrum_data: Optional SpectrumData object.
            peaks: Optional list of detected peaks.
            image_paths: Optional list of image paths to include.
        """
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()

            # Set font
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, title, ln=True, align='C')
            pdf.ln(5)

            # Add signal information
            if signal_data:
                PDFExporter._add_signal_info(pdf, signal_data)

            # Add spectrum information
            if spectrum_data:
                PDFExporter._add_spectrum_info(pdf, spectrum_data)

            # Add peaks table
            if peaks:
                PDFExporter._add_peaks_table(pdf, peaks)

            # Add images
            if image_paths:
                pdf.add_page()
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(0, 10, 'Plots', ln=True)
                pdf.ln(5)

                for img_path in image_paths:
                    if Path(img_path).exists():
                        try:
                            pdf.image(img_path, x=10, w=190)
                            pdf.ln(5)
                        except Exception as e:
                            logger.warning(f"Could not add image {img_path}: {e}")

            # Save PDF
            pdf.output(output_path)
            logger.info(f"PDF report exported: {output_path}")

        except Exception as e:
            logger.error(f"Error creating PDF report: {str(e)}")
            raise

    @staticmethod
    def _add_signal_info(pdf: FPDF, signal_data: SignalData) -> None:
        """Add signal information section to PDF.
        
        Args:
            pdf: FPDF instance.
            signal_data: SignalData object.
        """
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Signal Information', ln=True)
        pdf.set_font('Arial', '', 10)

        info = [
            f"Label: {signal_data.label}",
            f"Source: {signal_data.source}",
            f"Sampling Frequency: {signal_data.fs} Hz",
            f"Number of Samples: {signal_data.num_samples}",
            f"Duration: {signal_data.duration:.4f} s",
            f"Nyquist Frequency: {signal_data.nyquist_freq:.2f} Hz",
            f"Power: {signal_data.get_power():.6f}",
        ]

        for line in info:
            pdf.cell(0, 8, line, ln=True)

        pdf.ln(5)

    @staticmethod
    def _add_spectrum_info(pdf: FPDF, spectrum_data: SpectrumData) -> None:
        """Add spectrum information section to PDF.
        
        Args:
            pdf: FPDF instance.
            spectrum_data: SpectrumData object.
        """
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Spectrum Information', ln=True)
        pdf.set_font('Arial', '', 10)

        info = [
            f"Window Function: {spectrum_data.window}",
            f"FFT Length: {spectrum_data.N}",
            f"Frequency Resolution: {spectrum_data.freq_resolution:.4f} Hz",
            f"Maximum Magnitude: {spectrum_data.max_magnitude:.6f}",
            f"Maximum Magnitude (dB): {spectrum_data.max_magnitude_db:.2f} dB",
            f"Number of Frequency Bins: {spectrum_data.num_bins}",
        ]

        for line in info:
            pdf.cell(0, 8, line, ln=True)

        pdf.ln(5)

    @staticmethod
    def _add_peaks_table(pdf: FPDF, peaks: List[PeakInfo]) -> None:
        """Add peaks table to PDF.
        
        Args:
            pdf: FPDF instance.
            peaks: List of PeakInfo objects.
        """
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Detected Peaks', ln=True)
        pdf.set_font('Arial', '', 9)

        # Table header
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(20, 8, 'Rank', border=1)
        pdf.cell(45, 8, 'Frequency (Hz)', border=1)
        pdf.cell(40, 8, 'Magnitude', border=1)
        pdf.cell(40, 8, 'Magnitude (dB)', border=1)
        pdf.cell(35, 8, 'Prominence', border=1, ln=True)

        # Table rows
        pdf.set_font('Arial', '', 9)
        for i, peak in enumerate(peaks[:20], 1):  # Limit to 20 peaks
            pdf.cell(20, 8, str(i), border=1)
            pdf.cell(45, 8, f"{peak.frequency:.2f}", border=1)
            pdf.cell(40, 8, f"{peak.magnitude:.4e}", border=1)
            pdf.cell(40, 8, f"{peak.magnitude_db:.2f}", border=1)
            pdf.cell(35, 8, f"{peak.prominence:.4e}", border=1, ln=True)

        if len(peaks) > 20:
            pdf.set_font('Arial', '', 9)
            pdf.cell(0, 8, f"... and {len(peaks) - 20} more peaks", ln=True)

        pdf.ln(5)
