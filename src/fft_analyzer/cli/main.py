"""Command-line interface for FFT Signal Analyzer."""

from pathlib import Path
from typing import List, Optional

import click
import numpy as np

from ..core import (
    SignalGenerator,
    SignalLoader,
    FFTEngine,
    FilterEngine,
    PeakDetector,
)
from ..export import Exporter
from ..visualization import Visualizer
from ..utils import logger


@click.group()
def cli():
    """FFT-Based Signal Analyzer CLI."""
    pass


@cli.command()
@click.option(
    "--freq",
    multiple=True,
    type=float,
    default=[50, 120],
    help="Component frequencies (Hz)",
)
@click.option(
    "--amp",
    multiple=True,
    type=float,
    default=[1.0, 0.5],
    help="Component amplitudes",
)
@click.option(
    "--snr",
    type=float,
    default=20,
    help="Signal-to-noise ratio (dB)",
)
@click.option(
    "--fs",
    type=float,
    default=1000,
    help="Sampling frequency (Hz)",
)
@click.option(
    "--duration",
    type=float,
    default=1.0,
    help="Signal duration (seconds)",
)
@click.option(
    "--output",
    type=click.Path(),
    default="outputs/signal.npy",
    help="Output file path",
)
def generate(freq, amp, snr, fs, duration, output):
    """Generate synthetic signal."""
    try:
        click.echo(f"Generating signal with {len(freq)} components...")

        # Prepare components
        components = [
            {"frequency": f, "amplitude": a, "phase": 0}
            for f, a in zip(freq, amp)
        ]

        # Generate
        signal_data = SignalGenerator.generate_signal(
            components=components,
            fs=fs,
            duration=duration,
            snr_db=snr,
            label="CLI Generated Signal",
        )

        # Save
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output.endswith(".npy"):
            np.save(output, signal_data.amplitude)
            click.echo(f"✓ Signal saved to {output}")
        else:
            # Default to CSV
            output_csv = str(output_path.with_suffix(".csv"))
            import pandas as pd
            df = pd.DataFrame({
                "time": signal_data.time,
                "amplitude": signal_data.amplitude,
            })
            df.to_csv(output_csv, index=False)
            click.echo(f"✓ Signal saved to {output_csv}")

        click.echo(f"  Duration: {signal_data.duration:.4f}s")
        click.echo(f"  Samples: {signal_data.num_samples}")
        click.echo(f"  SNR: {snr} dB")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--window",
    type=click.Choice(["hann", "hamming", "blackman", "rectangle"]),
    default="hann",
    help="Window function",
)
@click.option(
    "--zero-pad",
    is_flag=True,
    default=True,
    help="Enable zero padding",
)
@click.option(
    "--fs",
    type=float,
    default=1000,
    help="Sampling frequency (Hz, if not in file)",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="outputs",
    help="Output directory for results",
)
def analyze(input_file, window, zero_pad, fs, output_dir):
    """Analyze signal from file."""
    try:
        click.echo(f"Analyzing {input_file}...")

        # Load signal
        if input_file.endswith(".csv"):
            signal_data = SignalLoader.load_csv(input_file, fs=fs)
        elif input_file.endswith(".wav"):
            signal_data = SignalLoader.load_wav(input_file)
        elif input_file.endswith(".npy"):
            signal_data = SignalLoader.load_npy(input_file, fs=fs)
        else:
            raise ValueError("Unsupported file format")

        SignalLoader.validate(signal_data)
        click.echo(f"  Duration: {signal_data.duration:.4f}s")
        click.echo(f"  Samples: {signal_data.num_samples}")
        click.echo(f"  Fs: {signal_data.fs} Hz")

        # Compute FFT
        click.echo("Computing FFT...")
        spectrum_data = FFTEngine.compute_fft(
            signal_data,
            window_type=window,
            zero_pad=zero_pad,
        )
        click.echo(f"  FFT length: {spectrum_data.N}")
        click.echo(f"  Frequency resolution: {spectrum_data.freq_resolution:.4f} Hz")

        # Detect peaks
        click.echo("Detecting peaks...")
        peaks = PeakDetector.detect_peaks(spectrum_data)
        click.echo(f"  Found {len(peaks)} peaks")

        # Display top 5 peaks
        for i, peak in enumerate(peaks[:5], 1):
            click.echo(
                f"    {i}. {peak.frequency:.2f} Hz: "
                f"{peak.magnitude_db:.2f} dB"
            )

        # Export
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        base_name = Path(input_file).stem

        click.echo("Exporting results...")
        Exporter.export_all(
            str(output_dir),
            spectrum_data=spectrum_data,
            peaks=peaks,
            signal_data=signal_data,
            base_filename=base_name,
        )

        click.echo(f"✓ Analysis complete. Results in {output_dir}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument("spectrum_file", type=click.Path(exists=True))
@click.option(
    "--peaks",
    is_flag=True,
    default=True,
    help="Annotate detected peaks",
)
@click.option(
    "--output",
    type=click.Path(),
    default="outputs/spectrum.html",
    help="Output file path",
)
def plot(spectrum_file, peaks, output):
    """Create interactive plot from spectrum data."""
    try:
        import pandas as pd

        click.echo(f"Creating plot from {spectrum_file}...")

        # Load spectrum data
        df = pd.read_csv(spectrum_file)

        freqs = df["Frequency_Hz"].values
        magnitude_db = df["Magnitude_dB"].values

        # Create figure
        import plotly.graph_objects as go
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=freqs,
            y=magnitude_db,
            mode='lines',
            name='Spectrum',
            line=dict(color='rgb(50, 100, 200)'),
        ))

        fig.update_layout(
            title="Frequency Spectrum",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude (dB)",
            template='plotly_white',
        )

        # Save
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))

        click.echo(f"✓ Plot saved to {output}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.option(
    "--host",
    default="127.0.0.1",
    help="Server host",
)
@click.option(
    "--port",
    type=int,
    default=8050,
    help="Server port",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug mode",
)
def dashboard(host, port, debug):
    """Launch interactive dashboard."""
    try:
        from ..ui import create_app

        click.echo(f"Launching dashboard at {host}:{port}...")

        app = create_app(debug=debug)
        app.run_server(debug=debug, host=host, port=port)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
def version():
    """Show version information."""
    click.echo("FFT Signal Analyzer v1.0.0")


if __name__ == "__main__":
    cli()
