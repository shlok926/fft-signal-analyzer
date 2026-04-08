"""
Export Module for FFT Signal Analyzer
Handles CSV, PNG, PDF, and HDF5 exports
"""

import io
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.io import write_image
import streamlit as st


class ExportManager:
    """Manages all export functionality for signal analysis results"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def export_to_csv(spectrum_data: Any, peaks: list) -> io.BytesIO:
        """
        Export spectrum data and peaks to CSV format
        
        Args:
            spectrum_data: SpectrumData object with frequency/magnitude/phase/psd
            peaks: List of detected peaks
            
        Returns:
            BytesIO buffer with CSV content
        """
        try:
            # Create spectrum DataFrame
            spectrum_df = pd.DataFrame({
                'Frequency (Hz)': spectrum_data.freqs,
                'Magnitude': spectrum_data.magnitude,
                'Magnitude (dB)': 20 * np.log10(np.maximum(spectrum_data.magnitude, 1e-10)),
                'Phase (rad)': spectrum_data.phase,
                'PSD (V²/Hz)': spectrum_data.psd,
            })
            
            # Create peaks DataFrame
            peaks_data = []
            for i, peak in enumerate(peaks[:20]):  # Top 20 peaks
                peaks_data.append({
                    'Rank': i + 1,
                    'Frequency (Hz)': peak.frequency,
                    'Magnitude': peak.magnitude,
                    'Magnitude (dB)': peak.magnitude_db,
                    'Prominence': peak.prominence,
                    'Q Factor': peak.q_factor if hasattr(peak, 'q_factor') else 'N/A',
                })
            
            peaks_df = pd.DataFrame(peaks_data)
            
            # Combine into single file with multiple sheets
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                spectrum_df.to_excel(writer, sheet_name='Spectrum', index=False)
                peaks_df.to_excel(writer, sheet_name='Detected Peaks', index=False)
            
            output.seek(0)
            return output
            
        except Exception as e:
            st.error(f"CSV Export Error: {str(e)}")
            return None
    
    @staticmethod
    def export_to_json(analysis_data: Dict[str, Any]) -> bytes:
        """
        Export complete analysis to JSON format
        """
        try:
            print("\n" + "="*60)
            print("🔹 JSON EXPORT FUNCTION CALLED")
            print("="*60)
            print(f"Input type: {type(analysis_data)}")
            print(f"Input is None: {analysis_data is None}")
            
            if not isinstance(analysis_data, dict):
                print(f"❌ ERROR: analysis_data is not a dict! Type: {type(analysis_data)}")
                return None
            
            # Safely extract data with defaults
            signal = analysis_data.get('signal')
            spectrum = analysis_data.get('spectrum')
            peaks = analysis_data.get('peaks', [])
            print(f"Extracted - Signal: {signal is not None}, Spectrum: {spectrum is not None}, Peaks: {len(peaks) if peaks else 0}")
            
            export_dict = {
                'timestamp': datetime.now().isoformat(),
            }
            
            # Add signal data if available
            if signal:
                try:
                    export_dict['signal'] = {
                        'time': signal.time.tolist() if hasattr(signal.time, 'tolist') else list(signal.time),
                        'amplitude': signal.amplitude.tolist() if hasattr(signal.amplitude, 'tolist') else list(signal.amplitude),
                        'sampling_rate': float(signal.fs) if hasattr(signal, 'fs') else 1000,
                        'duration': float(signal.duration) if hasattr(signal, 'duration') else 1.0,
                    }
                    print("✅ Signal data added")
                except Exception as e:
                    print(f"⚠️ Signal data error: {e}")
            
            # Add spectrum data if available
            if spectrum:
                try:
                    export_dict['spectrum'] = {
                        'frequencies': spectrum.freqs.tolist() if hasattr(spectrum.freqs, 'tolist') else list(spectrum.freqs),
                        'magnitudes': spectrum.magnitude.tolist() if hasattr(spectrum.magnitude, 'tolist') else list(spectrum.magnitude),
                        'phases': spectrum.phase.tolist() if hasattr(spectrum.phase, 'tolist') else list(spectrum.phase),
                        'psd': spectrum.psd.tolist() if hasattr(spectrum.psd, 'tolist') else list(spectrum.psd),
                    }
                    print("✅ Spectrum data added")
                except Exception as e:
                    print(f"⚠️ Spectrum data error: {e}")
            
            # Add peaks data
            if peaks:
                try:
                    export_dict['peaks'] = [
                        {
                            'frequency': float(p.frequency),
                            'magnitude': float(p.magnitude),
                            'magnitude_db': float(p.magnitude_db),
                            'prominence': float(p.prominence),
                        }
                        for p in peaks[:20]
                    ]
                    print(f"✅ {len(export_dict['peaks'])} peaks added")
                except Exception as e:
                    print(f"⚠️ Peaks data error: {e}")
            
            json_str = json.dumps(export_dict, indent=2)
            json_bytes = json_str.encode('utf-8')
            
            print(f"✅ JSON string created, length: {len(json_str)} chars")
            print(f"✅ JSON bytes created, length: {len(json_bytes)} bytes")
            print(f"✅ json_bytes type: {type(json_bytes)}")
            print(f"✅ json_bytes bool value (will show in download button): {bool(json_bytes)}")
            print("="*60)
            
            return json_bytes
            
        except Exception as e:
            print("="*60)
            print(f"❌ JSON Export CRITICAL ERROR: {str(e)}")
            print("="*60)
            import traceback
            traceback.print_exc()
            st.error(f"JSON Export Error: {str(e)}")
            return None
    
    @staticmethod
    def export_plots_to_html(figures: Dict[str, go.Figure]) -> bytes:
        """
        Export all plots as interactive HTML
        """
        try:
            print("🔹 Starting HTML export...")
            print(f"📊 Received {len(figures)} figures")
            
            if not figures:
                print("⚠️ No figures provided")
                st.warning("No figures available to export.")
                return None
            
            html_parts = []
            html_parts.append("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RF Spectrum Analysis Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html, body {
            width: 100%;
            height: 100%;
        }
        body {
            background-color: #0A0E27;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #00D4FF;
            padding-bottom: 20px;
        }
        h1 {
            font-size: 2.5em;
            color: #00D4FF;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            margin-bottom: 10px;
        }
        .subtitle {
            color: #B0B9C6;
            font-size: 0.95em;
        }
        .timestamp {
            color: #39FF14;
            font-size: 0.85em;
            margin-top: 15px;
        }
        .plot-container {
            background-color: #1A1F3A;
            border-left: 4px solid #00D4FF;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .plot-container h2 {
            color: #39FF14;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .plotly-graph-div {
            width: 100% !important;
            height: 500px !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📡 RF Spectrum Analysis Report</h1>
            <p class="subtitle">Real-Time Signal Processing and Frequency Analysis</p>
            <p class="timestamp">Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </header>
""")
            
            # Add each plot
            print(f"📊 Processing {len(figures)} figures...")
            plot_count = 0
            
            for plot_name, fig in figures.items():
                if fig is not None:
                    print(f"  ✓ Adding: {plot_name}")
                    try:
                        # Convert figure to HTML safely
                        plot_html = fig.to_html(include_plotlyjs=False, div_id=plot_name.replace(" ", "_").replace("(", "").replace(")", ""))
                        
                        html_parts.append(f"""
        <div class="plot-container">
            <h2>{plot_name}</h2>
            {plot_html}
        </div>
""")
                        plot_count += 1
                        print(f"    ✅ {plot_name} added successfully")
                    except Exception as e:
                        print(f"  ✗ Error processing {plot_name}: {e}")
                        # Add error message instead of failing
                        html_parts.append(f"""
        <div class="plot-container" style="background-color: #3a1a1a; border-left-color: #FF006E;">
            <h2>{plot_name}</h2>
            <p style="color: #FF006E;">Error rendering plot: {str(e)}</p>
        </div>
""")
            
            html_parts.append("""
    </div>
</body>
</html>
""")
            
            html_str = "".join(html_parts)
            html_bytes = html_str.encode('utf-8', errors='replace')
            
            print(f"✅ HTML export successful! {plot_count}/{len(figures)} plots added, Size: {len(html_bytes)} bytes")
            return html_bytes
            
        except Exception as e:
            print(f"❌ HTML Export Critical Error: {str(e)}")
            import traceback
            traceback.print_exc()
            st.error(f"HTML Export Error: {str(e)}")
            return None
    
    @staticmethod
    def export_metadata(signal_params: Dict, filter_params: Dict) -> Dict[str, Any]:
        """
        Create metadata about the analysis
        
        Args:
            signal_params: Signal generation parameters
            filter_params: Filter parameters
            
        Returns:
            Dictionary with metadata
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'software': 'AI-Enhanced Spectrum Analyzer',
            'version': '1.0.0',
            'signal_params': signal_params,
            'filter_params': filter_params,
            'export_formats': ['CSV', 'JSON', 'HTML', 'Interactive'],
        }


def create_export_ui():
    """Create the export UI modal/sidebar section"""
    return {
        'csv': st.checkbox("📄 CSV (Excel)", value=True, help="Export spectrum and peaks to CSV"),
        'json': st.checkbox("📋 JSON", value=False, help="Export complete analysis to JSON"),
        'html': st.checkbox("🌐 Interactive HTML", value=False, help="Export plots as interactive HTML"),
        'images': st.checkbox("🖼️ PNG Images", value=False, help="Export plots as PNG images"),
        'include_metadata': st.checkbox("📝 Include Metadata", value=True, help="Add analysis metadata"),
    }


def generate_export_report(
    analysis_data: Dict[str, Any],
    export_options: Dict[str, bool],
    signal_params: Dict,
    filter_params: Dict
) -> Dict[str, Any]:
    """
    Generate complete export package
    
    Args:
        analysis_data: Complete analysis results
        export_options: Which formats to export
        signal_params: Signal configuration
        filter_params: Filter configuration
        
    Returns:
        Dictionary with export files
    """
    exports = {}
    manager = ExportManager()
    
    try:
        # CSV Export
        if export_options.get('csv', True):
            csv_buffer = manager.export_to_csv(
                analysis_data['spectrum'],
                analysis_data['peaks']
            )
            if csv_buffer:
                exports['analysis_data.xlsx'] = csv_buffer
        
        # JSON Export
        if export_options.get('json', False):
            json_buffer = manager.export_to_json(analysis_data)
            if json_buffer:
                exports['analysis_data.json'] = json_buffer
        
        # Metadata
        if export_options.get('include_metadata', True):
            metadata = manager.export_metadata(signal_params, filter_params)
            exports['metadata'] = metadata
        
        return exports
        
    except Exception as e:
        st.error(f"Export Error: {str(e)}")
        return {}


if __name__ == "__main__":
    print("Export Manager Loaded Successfully")
