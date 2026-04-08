"""Integration tests for full analysis pipeline."""

import numpy as np
import pytest
from pathlib import Path
import tempfile

from fft_analyzer.core import (
    SignalGenerator,
    SignalLoader,
    FFTEngine,
    FilterEngine,
    PeakDetector,
)
from fft_analyzer.export import Exporter
from fft_analyzer.visualization import Visualizer


class TestFullPipeline:
    """Tests for end-to-end signal analysis."""

    def test_generate_analyze_export(self):
        """Test full pipeline: generate → analyze → export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate signal
            components = [
                {"frequency": 50, "amplitude": 1.0, "phase": 0},
                {"frequency": 120, "amplitude": 0.5, "phase": 0},
            ]

            signal = SignalGenerator.generate_signal(
                components=components,
                fs=1000,
                duration=1.0,
                snr_db=20,
                label="Test Signal",
            )

            # Analyze
            spectrum = FFTEngine.compute_fft(signal, window_type="hann")
            peaks = PeakDetector.detect_peaks(spectrum)

            # Export
            output_dir = Path(tmpdir) / "analysis"
            files = Exporter.export_all(
                str(output_dir),
                spectrum_data=spectrum,
                peaks=peaks,
                signal_data=signal,
                base_filename="test",
            )

            # Verify exports
            assert "spectrum_csv" in files
            assert (output_dir / "test_spectrum.csv").exists()
            assert (output_dir / "test_peaks.csv").exists()

    def test_signal_file_import_analyze(self):
        """Test importing signal from file and analyzing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test CSV file
            csv_path = Path(tmpdir) / "test_signal.csv"

            ts = np.linspace(0, 1, 1000)
            signal_vals = np.sin(2 * np.pi * 50 * ts) + 0.5 * np.sin(2 * np.pi * 120 * ts)

            import pandas as pd
            df = pd.DataFrame({"time": ts, "amplitude": signal_vals})
            df.to_csv(csv_path, index=False)

            # Load and analyze
            signal = SignalLoader.load_csv(str(csv_path), fs=1000)
            SignalLoader.validate(signal)

            spectrum = FFTEngine.compute_fft(signal)
            peaks = PeakDetector.detect_peaks(spectrum)

            assert len(peaks) > 0

    def test_filter_before_after_comparison(self):
        """Test filtering and compare spectra."""
        components = [
            {"frequency": 50, "amplitude": 1.0, "phase": 0},
            {"frequency": 120, "amplitude": 1.0, "phase": 0},
            {"frequency": 250, "amplitude": 1.0, "phase": 0},
        ]

        raw_signal = SignalGenerator.generate_signal(
            components=components,
            fs=1000,
            duration=1.0,
            snr_db=100,
        )

        # Apply low-pass filter (cutoff 150 Hz)
        filtered_signal = FilterEngine.low_pass(
            raw_signal,
            cutoff_hz=150,
            order=4,
        )

        # Compute spectra
        raw_spectrum = FFTEngine.compute_fft(raw_signal)
        filtered_spectrum = FFTEngine.compute_fft(filtered_signal)

        # Get 250 Hz component in each
        idx_250_raw = raw_spectrum.get_bin_at_frequency(250)
        idx_250_filt = filtered_spectrum.get_bin_at_frequency(250)

        mag_250_raw = raw_spectrum.magnitude[idx_250_raw]
        mag_250_filt = filtered_spectrum.magnitude[idx_250_filt]

        # Filtered should have less energy at 250 Hz
        assert mag_250_filt < mag_250_raw * 0.7

    def test_visualization_generation(self, sample_spectrum, sample_peaks):
        """Test that visualizations can be created."""
        # Create plots
        fig_time = Visualizer.plot_frequency_domain(sample_spectrum, sample_peaks)
        fig_phase = Visualizer.plot_phase_spectrum(sample_spectrum)
        fig_psd = Visualizer.plot_psd(sample_spectrum)

        # Check that figures are valid
        assert fig_time is not None
        assert fig_phase is not None
        assert fig_psd is not None

        # Check that they have data traces
        assert len(fig_time.data) > 0
        assert len(fig_phase.data) > 0
        assert len(fig_psd.data) > 0


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_invalid_signal_raises_error(self):
        """Test that invalid signal raises appropriate error."""
        with pytest.raises(ValueError):
            SignalData(
                time=np.array([0, 1]),
                amplitude=np.array([0]),  # Mismatch!
                fs=1000,
                label="Invalid",
                source="generated",
            )

    def test_empty_file_handling(self):
        """Test handling of empty/malformed files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create empty CSV
            csv_path = Path(tmpdir) / "empty.csv"
            csv_path.write_text("")

            with pytest.raises(Exception):
                SignalLoader.load_csv(str(csv_path))

    def test_very_short_signal(self):
        """Test that very short signals are rejected."""
        with pytest.raises(ValueError):
            signal = SignalData(
                time=np.array([0, 1]),
                amplitude=np.array([0, 1]),
                fs=1000,
                label="Too short",
                source="generated",
            )
            SignalLoader.validate(signal)

    def test_all_zero_signal_warning(self):
        """Test warning on all-zero signal."""
        signal = SignalData(
            time=np.linspace(0, 1, 1000),
            amplitude=np.zeros(1000),
            fs=1000,
            label="Zero signal",
            source="generated",
        )

        # Should warn but not crash
        result = SignalLoader.validate(signal)
        assert result is True  # Validation succeeds (just logs warning)


from fft_analyzer.models import SignalData
