"""Frequency-domain plot builder."""

from typing import List, Optional

import plotly.graph_objects as go

from ..models import SpectrumData, PeakInfo


class FreqDomainPlot:
    """Create frequency-domain spectrum plots."""

    @staticmethod
    def create(
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
        fig = go.Figure()

        # Add magnitude spectrum (dB scale)
        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=spectrum_data.magnitude_db,
            mode='lines',
            name='Magnitude (dB)',
            line=dict(color='rgb(50, 100, 200)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>A: %{y:.2f}dB<extra></extra>',
        ))

        # Add detected peaks if provided
        if peaks:
            peak_freqs = [p.frequency for p in peaks]
            peak_mags_db = [p.magnitude_db for p in peaks]
            peak_labels = [
                f"f={p.frequency:.1f}Hz<br>"
                f"A={p.magnitude:.4f}<br>"
                f"{p.magnitude_db:.1f}dB"
                for p in peaks
            ]

            fig.add_trace(go.Scatter(
                x=peak_freqs,
                y=peak_mags_db,
                mode='markers+text',
                name='Peaks',
                marker=dict(
                    size=10,
                    color='rgb(255, 100, 50)',
                    symbol='star',
                    line=dict(color='white', width=2),
                ),
                text=[f"{i+1}" for i in range(len(peaks))],
                textposition='top center',
                textfont=dict(size=10, color='rgb(255, 100, 50)'),
                hovertext=peak_labels,
                hovertemplate='<b>Peak %{text}</b><br>%{hovertext}<extra></extra>',
            ))

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude (dB)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_linear(
        spectrum_data: SpectrumData,
        peaks: Optional[List[PeakInfo]] = None,
        title: str = "Frequency Spectrum (Linear)",
    ) -> go.Figure:
        """Create frequency plot with linear magnitude scale.
        
        Args:
            spectrum_data: SpectrumData object.
            peaks: Optional list of PeakInfo objects to annotate.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        fig = go.Figure()

        # Add magnitude spectrum (linear scale)
        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=spectrum_data.magnitude,
            mode='lines',
            name='Magnitude',
            line=dict(color='rgb(50, 100, 200)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>A: %{y:.4f}<extra></extra>',
        ))

        # Add detected peaks if provided
        if peaks:
            peak_freqs = [p.frequency for p in peaks]
            peak_mags = [p.magnitude for p in peaks]
            peak_labels = [
                f"f={p.frequency:.1f}Hz<br>"
                f"A={p.magnitude:.4f}"
                for p in peaks
            ]

            fig.add_trace(go.Scatter(
                x=peak_freqs,
                y=peak_mags,
                mode='markers+text',
                name='Peaks',
                marker=dict(
                    size=10,
                    color='rgb(255, 100, 50)',
                    symbol='star',
                    line=dict(color='white', width=2),
                ),
                text=[f"{i+1}" for i in range(len(peaks))],
                textposition='top center',
                hovertext=peak_labels,
                hovertemplate='<b>Peak %{text}</b><br>%{hovertext}<extra></extra>',
            ))

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude (Linear)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig
