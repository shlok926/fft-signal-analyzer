"""Dash callbacks for interactive updates."""

import json
from typing import Optional

import numpy as np
from dash import callback, Input, Output, State, dash_table, html
import plotly.graph_objects as go

from ..core import (
    SignalGenerator,
    FFTEngine,
    FilterEngine,
    PeakDetector,
)
from ..models import SignalData, SpectrumData, PeakInfo
from ..visualization import Visualizer
from ..utils import logger


def register_callbacks(app):
    """Register all Dash callbacks.
    
    Args:
        app: Dash application instance.
    """

    @callback(
        Output("div-generate-params", "style"),
        Output("div-import-file", "style"),
        Input("radio-signal-source", "value"),
    )
    def toggle_signal_source(source_type):
        """Toggle between Generate and Import File modes."""
        if source_type == "import":
            return {"display": "none"}, {"display": "block"}
        else:
            return {"display": "block"}, {"display": "none"}

    @callback(
        Output("modal-settings", "is_open"),
        Input("btn-settings", "n_clicks"),
        Input("settings-close", "n_clicks"),
        Input("settings-save", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_settings_modal(open_clicks, close_clicks, save_clicks):
        """Open/close settings modal."""
        if open_clicks and open_clicks > (close_clicks or 0) and open_clicks > (save_clicks or 0):
            return True
        return False

    @callback(
        Output("store-settings", "data"),
        Input("settings-save", "n_clicks"),
        State("settings-peak-threshold", "value"),
        State("settings-zero-pad", "value"),
        State("settings-export-format", "value"),
        prevent_initial_call=True,
    )
    def save_settings(n_clicks, threshold, zero_pad, export_fmt):
        """Save settings to store."""
        settings = {
            "peak_threshold": threshold or 0.1,
            "zero_padding": bool(zero_pad),
            "export_format": export_fmt or "csv",
        }
        logger.info(f"Settings saved: {settings}")
        return settings

    @callback(
        Output("store-signal-data", "data"),
        Output("store-spectrum-data", "data"),
        Output("store-peaks-data", "data"),
        Input("btn-analyze", "n_clicks"),
        State("input-freq1", "value"),
        State("input-amp1", "value"),
        State("input-freq2", "value"),
        State("input-amp2", "value"),
        State("input-snr", "value"),
        State("input-fs", "value"),
        State("input-duration", "value"),
        State("dropdown-window", "value"),
        State("dropdown-filter-type", "value"),
        State("input-cutoff", "value"),
        prevent_initial_call=True,
    )
    def analyze_signal(
        n_clicks,
        freq1,
        amp1,
        freq2,
        amp2,
        snr_db,
        fs,
        duration,
        window,
        filter_type,
        cutoff,
    ):
        """Analyze signal: generate → FFT → detect peaks."""
        try:
            # Generate signal
            components = [
                {"frequency": freq1, "amplitude": amp1, "phase": 0},
                {"frequency": freq2, "amplitude": amp2, "phase": 0},
            ]

            signal_data = SignalGenerator.generate_signal(
                components=components,
                fs=fs,
                duration=duration,
                snr_db=snr_db,
                label="Generated Signal",
            )

            # Apply filter if specified
            if filter_type != "none":
                if filter_type == "lowpass":
                    signal_data = FilterEngine.low_pass(signal_data, cutoff)
                elif filter_type == "highpass":
                    signal_data = FilterEngine.high_pass(signal_data, cutoff)
                # Add other filter types as needed

            # Compute FFT
            spectrum_data = FFTEngine.compute_fft(signal_data, window_type=window)

            # Detect peaks
            peaks = PeakDetector.detect_peaks(spectrum_data)

            # Store as JSON
            signal_json = {
                "time": signal_data.time.tolist(),
                "amplitude": signal_data.amplitude.tolist(),
                "fs": signal_data.fs,
                "label": signal_data.label,
            }

            spectrum_json = {
                "freqs": spectrum_data.freqs.tolist(),
                "magnitude": spectrum_data.magnitude.tolist(),
                "magnitude_db": spectrum_data.magnitude_db.tolist(),
                "phase": spectrum_data.phase.tolist(),
                "psd": spectrum_data.psd.tolist(),
                "window": spectrum_data.window,
                "N": spectrum_data.N,
            }

            peaks_json = [
                {
                    "frequency": p.frequency,
                    "magnitude": p.magnitude,
                    "magnitude_db": p.magnitude_db,
                    "prominence": p.prominence,
                    "index": p.index,
                }
                for p in peaks
            ]

            return signal_json, spectrum_json, peaks_json

        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            return None, None, None

    @callback(
        Output("graph-time-domain", "figure"),
        Input("store-signal-data", "data"),
    )
    def update_time_plot(signal_json):
        """Update time domain plot."""
        if not signal_json:
            return go.Figure().update_layout(title="Time Domain Signal")

        try:
            signal_data = SignalData(
                time=np.array(signal_json["time"]),
                amplitude=np.array(signal_json["amplitude"]),
                fs=signal_json["fs"],
                label=signal_json["label"],
                source="generated",
            )
            return Visualizer.plot_time_domain(signal_data)
        except Exception as e:
            logger.error(f"Error updating time plot: {str(e)}")
            return go.Figure()

    @callback(
        Output("graph-freq-domain", "figure"),
        Input("store-spectrum-data", "data"),
        Input("store-peaks-data", "data"),
    )
    def update_freq_plot(spectrum_json, peaks_json):
        """Update frequency domain plot."""
        if not spectrum_json:
            return go.Figure().update_layout(title="Frequency Spectrum")

        try:
            spectrum_data = SpectrumData(
                freqs=np.array(spectrum_json["freqs"]),
                magnitude=np.array(spectrum_json["magnitude"]),
                magnitude_db=np.array(spectrum_json["magnitude_db"]),
                phase=np.array(spectrum_json["phase"]),
                psd=np.array(spectrum_json["psd"]),
                window=spectrum_json["window"],
                N=spectrum_json["N"],
            )

            peaks = None
            if peaks_json:
                peaks = [
                    PeakInfo(
                        frequency=p["frequency"],
                        magnitude=p["magnitude"],
                        magnitude_db=p["magnitude_db"],
                        prominence=p["prominence"],
                        index=p["index"],
                    )
                    for p in peaks_json
                ]

            return Visualizer.plot_frequency_domain(spectrum_data, peaks)
        except Exception as e:
            logger.error(f"Error updating frequency plot: {str(e)}")
            return go.Figure()

    @callback(
        Output("graph-phase", "figure"),
        Input("store-spectrum-data", "data"),
    )
    def update_phase_plot(spectrum_json):
        """Update phase spectrum plot."""
        if not spectrum_json:
            return go.Figure().update_layout(title="Phase Spectrum")

        try:
            spectrum_data = SpectrumData(
                freqs=np.array(spectrum_json["freqs"]),
                magnitude=np.array(spectrum_json["magnitude"]),
                magnitude_db=np.array(spectrum_json["magnitude_db"]),
                phase=np.array(spectrum_json["phase"]),
                psd=np.array(spectrum_json["psd"]),
                window=spectrum_json["window"],
                N=spectrum_json["N"],
            )
            return Visualizer.plot_phase_spectrum(spectrum_data)
        except Exception as e:
            logger.error(f"Error updating phase plot: {str(e)}")
            return go.Figure()

    @callback(
        Output("graph-psd", "figure"),
        Input("store-spectrum-data", "data"),
    )
    def update_psd_plot(spectrum_json):
        """Update PSD plot."""
        if not spectrum_json:
            return go.Figure().update_layout(title="Power Spectral Density")

        try:
            spectrum_data = SpectrumData(
                freqs=np.array(spectrum_json["freqs"]),
                magnitude=np.array(spectrum_json["magnitude"]),
                magnitude_db=np.array(spectrum_json["magnitude_db"]),
                phase=np.array(spectrum_json["phase"]),
                psd=np.array(spectrum_json["psd"]),
                window=spectrum_json["window"],
                N=spectrum_json["N"],
            )
            return Visualizer.plot_psd(spectrum_data)
        except Exception as e:
            logger.error(f"Error updating PSD plot: {str(e)}")
            return go.Figure()

    @callback(
        Output("div-peaks-table", "children"),
        Input("store-peaks-data", "data"),
    )
    def update_peaks_table(peaks_json):
        """Update peaks table."""
        if not peaks_json:
            return html.P("No peaks detected")

        try:
            df_data = [
                {
                    "Rank": i + 1,
                    "Frequency (Hz)": f"{p['frequency']:.2f}",
                    "Magnitude": f"{p['magnitude']:.4f}",
                    "Magnitude (dB)": f"{p['magnitude_db']:.2f}",
                    "Prominence": f"{p['prominence']:.4e}",
                }
                for i, p in enumerate(peaks_json[:20])
            ]

            table = dash_table.DataTable(
                data=df_data,
                columns=[
                    {"name": "Rank", "id": "Rank"},
                    {"name": "Frequency (Hz)", "id": "Frequency (Hz)"},
                    {"name": "Magnitude", "id": "Magnitude"},
                    {"name": "Magnitude (dB)", "id": "Magnitude (dB)"},
                    {"name": "Prominence", "id": "Prominence"},
                ],
                style_cell={"textAlign": "left", "fontSize": 12},
                style_header={"fontWeight": "bold"},
                style_table={"overflowX": "auto"},
            )

            total = len(peaks_json)
            shown = min(20, total)
            summary = html.P(f"Showing {shown} of {total} peaks")

            return [summary, table]

        except Exception as e:
            logger.error(f"Error updating peaks table: {str(e)}")
            return html.P(f"Error: {str(e)}")

    @callback(
        Output("file-upload-status", "children"),
        Input("signal-file-upload", "contents"),
        State("signal-file-upload", "filename"),
        prevent_initial_call=True,
    )
    def handle_file_upload(contents, filename):
        """Handle CSV/WAV file upload."""
        if not contents:
            return "No file uploaded"

        try:
            from base64 import b64decode
            from io import StringIO, BytesIO
            import pandas as pd

            # Decode file
            if filename.endswith(".csv"):
                # CSV file
                content_string = contents.split(",")[1]
                decoded = b64decode(content_string).decode("utf-8")
                df = pd.read_csv(StringIO(decoded))
                
                # Assume last column is amplitude
                amplitude = df.iloc[:, -1].values
                fs = 1000.0  # Default sampling rate
                
                return f"✅ Loaded {filename}: {len(amplitude)} samples"
            else:
                return "❌ Unsupported file format. Use CSV."

        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return f"❌ Upload failed: {str(e)}"

    @callback(
        Output("file-download-status", "children"),
        Input("btn-export", "n_clicks"),
        State("store-spectrum-data", "data"),
        prevent_initial_call=True,
    )
    def export_analysis(n_clicks, spectrum_json):
        """Export analysis plots and data."""
        if not spectrum_json:
            return "❌ Run analysis first!"

        try:
            from ..export import Exporter
            import os

            # Create export directory
            os.makedirs("outputs/exports", exist_ok=True)

            # Reconstruct spectrum data
            spectrum_data = SpectrumData(
                freqs=np.array(spectrum_json["freqs"]),
                magnitude=np.array(spectrum_json["magnitude"]),
                magnitude_db=np.array(spectrum_json["magnitude_db"]),
                phase=np.array(spectrum_json["phase"]),
                psd=np.array(spectrum_json["psd"]),
                window=spectrum_json["window"],
                N=spectrum_json["N"],
            )

            # Export CSV
            exporter = Exporter()
            csv_path = "outputs/exports/spectrum_data.csv"
            exporter.export_spectrum_csv(spectrum_data, csv_path)

            logger.info(f"✅ Exported to {csv_path}")
            return f"✅ Exported! Check outputs/exports/ folder"

        except Exception as e:
            logger.error(f"Error exporting: {str(e)}")
            return f"❌ Export failed: {str(e)}"
