"""Phase spectrum plot builder."""

import plotly.graph_objects as go

from ..models import SpectrumData


class PhasePlot:
    """Create phase spectrum plots."""

    @staticmethod
    def create(
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
        fig = go.Figure()

        # Add phase trace
        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=spectrum_data.phase,
            mode='lines',
            name='Phase',
            line=dict(color='rgb(150, 100, 50)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>φ: %{y:.4f}rad<extra></extra>',
        ))

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Phase (radians)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_degrees(
        spectrum_data: SpectrumData,
        title: str = "Phase Spectrum (Degrees)",
    ) -> go.Figure:
        """Create phase spectrum plot with degrees scale.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        import numpy as np

        phase_degrees = np.degrees(spectrum_data.phase)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=phase_degrees,
            mode='lines',
            name='Phase',
            line=dict(color='rgb(150, 100, 50)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>φ: %{y:.2f}°<extra></extra>',
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Phase (degrees)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_unwrapped(
        spectrum_data: SpectrumData,
        title: str = "Unwrapped Phase Spectrum",
    ) -> go.Figure:
        """Create unwrapped phase spectrum plot.
        
        Args:
            spectrum_data: SpectrumData object.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        import numpy as np

        # Unwrap phase
        phase_unwrapped = np.unwrap(spectrum_data.phase)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spectrum_data.freqs,
            y=phase_unwrapped,
            mode='lines',
            name='Phase (unwrapped)',
            line=dict(color='rgb(150, 100, 50)', width=1.5),
            hovertemplate='f: %{x:.2f}Hz<br>φ: %{y:.4f}rad<extra></extra>',
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Phase (radians, unwrapped)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig
