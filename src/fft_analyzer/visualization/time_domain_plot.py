"""Time-domain plot builder."""

import plotly.graph_objects as go

from ..models import SignalData


class TimeDomainPlot:
    """Create time-domain signal plots."""

    @staticmethod
    def create(
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
        fig = go.Figure()

        # Add signal trace
        fig.add_trace(go.Scatter(
            x=signal_data.time,
            y=signal_data.amplitude,
            mode='lines',
            name=signal_data.label,
            line=dict(color='rgb(50, 100, 200)', width=1),
            hovertemplate='t: %{x:.6f}s<br>A: %{y:.4f}<extra></extra>',
        ))

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        # Enable interactive features
        fig.update_xaxes(rangeslider_visible=False)

        return fig

    @staticmethod
    def create_multiplot(
        signals: list[SignalData],
        title: str = "Multi-Signal Comparison",
    ) -> go.Figure:
        """Create plot with multiple signals.
        
        Args:
            signals: List of SignalData objects.
            title: Plot title.
            
        Returns:
            Plotly Figure object.
        """
        fig = go.Figure()

        colors = [
            'rgb(50, 100, 200)',
            'rgb(200, 50, 50)',
            'rgb(50, 150, 50)',
            'rgb(200, 100, 50)',
            'rgb(150, 50, 150)',
        ]

        for i, signal in enumerate(signals):
            color = colors[i % len(colors)]
            fig.add_trace(go.Scatter(
                x=signal.time,
                y=signal.amplitude,
                mode='lines',
                name=signal.label,
                line=dict(color=color, width=1),
                hovertemplate='t: %{x:.6f}s<br>A: %{y:.4f}<extra></extra>',
            ))

        fig.update_layout(
            title=title,
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
        )

        return fig
