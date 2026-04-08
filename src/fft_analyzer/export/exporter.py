"""Main export orchestrator."""

from pathlib import Path
from typing import List, Optional

from ..models import SpectrumData, PeakInfo, SignalData
from ..utils import logger
from .csv_exporter import CSVExporter
from .image_exporter import ImageExporter
from .pdf_exporter import PDFExporter
import plotly.graph_objects as go


class Exporter:
    """Main export orchestrator for all output formats."""

    @staticmethod
    def export_all(
        output_dir: str,
        spectrum_data: Optional[SpectrumData] = None,
        peaks: Optional[List[PeakInfo]] = None,
        figures: Optional[dict[str, go.Figure]] = None,
        signal_data: Optional[SignalData] = None,
        base_filename: str = "analysis",
    ) -> dict[str, str]:
        """Export analysis results in all formats.
        
        Args:
            output_dir: Output directory path.
            spectrum_data: Optional SpectrumData object.
            peaks: Optional list of detected peaks.
            figures: Optional dict mapping names to Figure objects.
            signal_data: Optional SignalData object.
            base_filename: Base name for output files.
            
        Returns:
            Dict mapping format names to output file paths.
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            output_files = {}

            # Export CSV
            if spectrum_data:
                csv_path = output_dir / f"{base_filename}_spectrum.csv"
                CSVExporter.export_spectrum(spectrum_data, str(csv_path), peaks)
                output_files['spectrum_csv'] = str(csv_path)

            # Export peaks CSV
            if peaks:
                peaks_csv_path = output_dir / f"{base_filename}_peaks.csv"
                CSVExporter.export_peaks(peaks, str(peaks_csv_path))
                output_files['peaks_csv'] = str(peaks_csv_path)

            # Export images
            if figures:
                plots_dir = output_dir / "plots"
                plots_dir.mkdir(exist_ok=True)
                ImageExporter.export_multiple(
                    figures,
                    str(plots_dir),
                    format='png',
                    scale=2
                )
                output_files['plots_dir'] = str(plots_dir)

            # Export PDF report
            if spectrum_data or signal_data or peaks:
                pdf_path = output_dir / f"{base_filename}_report.pdf"
                image_paths = []
                if figures:
                    # Generate temporary images for PDF
                    plots_dir = output_dir / "plots"
                    image_paths = [
                        str(plots_dir / f"{name}.png")
                        for name in figures.keys()
                    ]
                    # Create these images
                    for name, fig in figures.items():
                        img_path = plots_dir / f"{name}.png"
                        if not img_path.exists():
                            try:
                                ImageExporter.export_png(fig, str(img_path))
                            except:
                                pass

                PDFExporter.create_report(
                    str(pdf_path),
                    signal_data=signal_data,
                    spectrum_data=spectrum_data,
                    peaks=peaks,
                    image_paths=image_paths,
                )
                output_files['report_pdf'] = str(pdf_path)

            logger.info(f"All exports completed. Output directory: {output_dir}")
            return output_files

        except Exception as e:
            logger.error(f"Error in export_all: {str(e)}")
            raise

    @staticmethod
    def export_spectrum_csv(
        spectrum_data: SpectrumData,
        output_path: str,
        peaks: Optional[List[PeakInfo]] = None,
    ) -> str:
        """Export spectrum to CSV.
        
        Args:
            spectrum_data: SpectrumData object.
            output_path: Path to output file.
            peaks: Optional list of peaks.
            
        Returns:
            Path to exported file.
        """
        CSVExporter.export_spectrum(spectrum_data, output_path, peaks)
        return output_path

    @staticmethod
    def export_figure_png(
        figure: go.Figure,
        output_path: str,
        width: int = 1200,
        height: int = 600,
    ) -> str:
        """Export figure to PNG.
        
        Args:
            figure: Plotly Figure object.
            output_path: Path to output file.
            width: Image width.
            height: Image height.
            
        Returns:
            Path to exported file.
        """
        ImageExporter.export_png(figure, output_path, width, height)
        return output_path

    @staticmethod
    def export_figure_svg(
        figure: go.Figure,
        output_path: str,
    ) -> str:
        """Export figure to SVG.
        
        Args:
            figure: Plotly Figure object.
            output_path: Path to output file.
            
        Returns:
            Path to exported file.
        """
        ImageExporter.export_svg(figure, output_path)
        return output_path

    @staticmethod
    def export_report_pdf(
        output_path: str,
        signal_data: Optional[SignalData] = None,
        spectrum_data: Optional[SpectrumData] = None,
        peaks: Optional[List[PeakInfo]] = None,
        image_paths: Optional[List[str]] = None,
    ) -> str:
        """Export analysis report to PDF.
        
        Args:
            output_path: Path to output file.
            signal_data: Optional SignalData.
            spectrum_data: Optional SpectrumData.
            peaks: Optional list of peaks.
            image_paths: Optional list of image paths.
            
        Returns:
            Path to exported file.
        """
        PDFExporter.create_report(
            output_path,
            signal_data=signal_data,
            spectrum_data=spectrum_data,
            peaks=peaks,
            image_paths=image_paths,
        )
        return output_path
