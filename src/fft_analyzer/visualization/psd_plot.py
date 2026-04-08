"""Power Spectral Density (PSD) plot builder."""

import plotly.graph_objects as go

from ..models import SpectrumData


class PSDPlot:
    """Create Power Spectral Density plots."""

    @staticmethod
    def create(
        spectrum_data: SpectrumData,
        title: str = "Power Spectral Density",
    ) -> go.Figure:
        """Create Power Spectral Density plot.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        fig = go.Figure()

        # Add PSD trace
        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=spectrum_data.psd,
            mode='lines',
            name='PSD',
            line=dict(color='rgb(100, 150, 100)', width=1.5),
            fill='tozeroy',
            hovertemplate='f: %{x:.2f}Hz<br>PSD: %{y:.4e}<extra></extra>',
        ))

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Power Spectral Density (V²/Hz)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_db(
        spectrum_data: SpectrumData,
        title: str = "Power Spectral Density (dB)",
    ) -> go.Figure:
        """Create PSD plot in dB scale.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        import numpy as np

        # Convert PSD to dB
        psd_db = 10 * np.log10(spectrum_data.psd + 1e-12)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=psd_db,
            mode='lines',
            name='PSD (dB)',
            line=dict(color='rgb(100, 150, 100)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>PSD: %{y:.2f}dB<extra></extra>',
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Power Spectral Density (dB)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_log_scale(
        spectrum_data: SpectrumData,
        title: str = "Power Spectral Density (Log Scale)",
    ) -> go.Figure:
        """Create PSD plot with log scale on both axes.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=spectrum_data.psd,
            mode='lines',
            name='PSD',
            line=dict(color='rgb(100, 150, 100)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>PSD: %{y:.4e}<extra></extra>',
        ))

        fig.update_xaxes(type='log')
        fig.update_yaxes(type='log')

        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz, log scale)",
            yaxis_title="Power Spectral Density (log scale)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig
