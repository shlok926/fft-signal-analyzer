"""Main visualization orchestrator."""

from typing import List, Optional

import plotly.graph_objects as go

from ..models import SignalData, SpectrumData, PeakInfo
from .time_domain_plot import TimeDomainPlot
from .freq_domain_plot import FreqDomainPlot
from .phase_plot import PhasePlot
from .psd_plot import PSDPlot


class Visualizer:
    """Main visualization orchestrator for creating all plot types."""

    @staticmethod
    def plot_time_domain(
        signal_data: SignalData,
        title: str = "Time Domain Signal",
    ) -> go.Figure:
        """Create interactive time-domain plot.
        
        Args:
            signal_data: SignalData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        return TimeDomainPlot.create(signal_data, title)

    @staticmethod
    def plot_frequency_domain(
        spectrum_data: SpectrumData,
        peaks: Optional[List[PeakInfo]] = None,
        title: str = "Frequency Spectrum",
    ) -> go.Figure:
        """Create interactive frequency-domain plot.
        
        Args:
            spectrum_data: SpectrumData object.
            peaks: Optional list of PeakInfo objects to annotate.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        return FreqDomainPlot.create(spectrum_data, peaks, title)

    @staticmethod
    def plot_phase_spectrum(
        spectrum_data: SpectrumData,
        title: str = "Phase Spectrum",
    ) -> go.Figure:
        """Create phase spectrum plot.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        return PhasePlot.create(spectrum_data, title)

    @staticmethod
    def plot_psd(
        spectrum_data: SpectrumData,
        title: str = "Power Spectral Density",
    ) -> go.Figure:
        """Create power spectral density plot.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        return PSDPlot.create(spectrum_data, title)

    @staticmethod
    def plot_comparison(
        raw_signal: SignalData,
        filtered_signal: SignalData,
        title: str = "Raw vs Filtered Signal",
    ) -> go.Figure:
        """Create comparison plot of raw vs filtered signal.
        
        Args:
            raw_signal: Original SignalData.
            filtered_signal: Filtered SignalData.
            title: Plot title.
            
        Returns:
            Plotly Figure object with time-domain comparison.
        """
        fig = go.Figure()

        # Raw signal
        fig.add_trace(go.Scatter(
            x=raw_signal.time,
            y=raw_signal.amplitude,
            mode='lines',
            name=raw_signal.label,
            line=dict(color='rgb(255, 100, 100)', width=1),
            hovertemplate='t: %{x:.6f}s<br>A: %{y:.4f}<extra></extra>',
        ))

        # Filtered signal
        fig.add_trace(go.Scatter(
            x=filtered_signal.time,
            y=filtered_signal.amplitude,
            mode='lines',
            name=filtered_signal.label,
            line=dict(color='rgb(100, 150, 255)', width=1.5),
            hovertemplate='t: %{x:.6f}s<br>A: %{y:.4f}<extra></extra>',
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            hovermode='x unified',
            template='plotly_white',
            height=500,
        )

        return fig

    @staticmethod
    def plot_spectrum_comparison(
        raw_spectrum: SpectrumData,
        filtered_spectrum: SpectrumData,
        raw_label: str = "Raw",
        filtered_label: str = "Filtered",
        title: str = "Frequency Spectrum Comparison",
    ) -> go.Figure:
        """Create comparison of raw vs filtered spectra.
        
        Args:
            raw_spectrum: SpectrumData of raw signal.
            filtered_spectrum: SpectrumData of filtered signal.
            raw_label: Label for raw spectrum.
            filtered_label: Label for filtered spectrum.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        fig = go.Figure()

        # Raw spectrum (dB)
        fig.add_trace(go.Scatter(
            x=raw_spectrum.freqs,
            y=raw_spectrum.magnitude_db,
            mode='lines',
            name=raw_label,
            line=dict(color='rgb(255, 100, 100)', width=1),
            hovertemplate='f: %{x:.2f}Hz<br>A: %{y:.2f}dB<extra></extra>',
        ))

        # Filtered spectrum (dB)
        fig.add_trace(go.Scatter(
            x=filtered_spectrum.freqs,
            y=filtered_spectrum.magnitude_db,
            mode='lines',
            name=filtered_label,
            line=dict(color='rgb(100, 150, 255)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>A: %{y:.2f}dB<extra></extra>',
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude (dB)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
        )

        return fig
