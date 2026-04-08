"""Image export functionality for plots."""

from pathlib import Path

import plotly.graph_objects as go

from ..utils import logger


class ImageExporter:
    """Export plots to image formats."""

    @staticmethod
    def export_png(
        figure: go.Figure,
        output_path: str,
        width: int = 1200,
        height: int = 600,
        scale: int = 2,
    ) -> None:
        """Export Plotly figure to PNG.
        
        Args:
            figure: Plotly Figure object.
            output_path: Path to output PNG file.
            width: Image width in pixels.
            height: Image height in pixels.
            scale: Scale factor (for DPI).
        """
        try:
            # Update figure dimensions
            figure.update_layout(width=width, height=height)

            # Export to PNG
            figure.write_image(
                output_path,
                format='png',
                scale=scale,
            )

            logger.info(f"Figure exported to PNG: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting to PNG: {str(e)}")
            raise

    @staticmethod
    def export_svg(
        figure: go.Figure,
        output_path: str,
        width: int = 1200,
        height: int = 600,
    ) -> None:
        """Export Plotly figure to SVG (vector format).
        
        Args:
            figure: Plotly Figure object.
            output_path: Path to output SVG file.
            width: Image width in pixels.
            height: Image height in pixels.
        """
        try:
            # Update figure dimensions
            figure.update_layout(width=width, height=height)

            # Export to SVG
            figure.write_image(
                output_path,
                format='svg',
            )

            logger.info(f"Figure exported to SVG: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting to SVG: {str(e)}")
            raise

    @staticmethod
    def export_html(
        figure: go.Figure,
        output_path: str,
        include_plotlyjs: str = 'cdn',
    ) -> None:
        """Export Plotly figure to interactive HTML.
        
        Args:
            figure: Plotly Figure object.
            output_path: Path to output HTML file.
            include_plotlyjs: How to include Plotly JS ('cdn', 'inline', 'require').
        """
        try:
            figure.write_html(
                output_path,
                include_plotlyjs=include_plotlyjs,
            )

            logger.info(f"Figure exported to HTML: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting to HTML: {str(e)}")
            raise

    @staticmethod
    def export_multiple(
        figures: dict[str, go.Figure],
        output_dir: str,
        format: str = 'png',
        **kwargs
    ) -> None:
        """Export multiple figures to a directory.
        
        Args:
            figures: Dict mapping filenames to Figure objects.
            output_dir: Output directory path.
            format: Image format ('png', 'svg', 'html').
            **kwargs: Additional arguments for export functions.
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            for name, fig in figures.items():
                if not name.lower().endswith(f".{format}"):
                    name += f".{format}"

                output_path = output_dir / name

                if format.lower() == 'png':
                    ImageExporter.export_png(fig, str(output_path), **kwargs)
                elif format.lower() == 'svg':
                    ImageExporter.export_svg(fig, str(output_path), **kwargs)
                elif format.lower() == 'html':
                    ImageExporter.export_html(fig, str(output_path), **kwargs)
                else:
                    logger.warning(f"Unknown format: {format}")

        except Exception as e:
            logger.error(f"Error exporting multiple figures: {str(e)}")
            raise
