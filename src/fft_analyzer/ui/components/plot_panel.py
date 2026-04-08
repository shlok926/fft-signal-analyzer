"""
Plot panel component for Dash UI.

Displays interactive visualization plots for signal analysis.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_plot_panel() -> dbc.Col:
    """
    Create the right plot panel with visualization containers.

    Returns:
        dbc.Col: Bootstrap column containing plot containers
    """
    return dbc.Col(
        [
            html.H4("Analysis Visualization", className="mb-4"),
            
            # Time Domain Plot
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H6("📈 Time Domain Signal", className="mb-0")
                    ),
                    dbc.CardBody(
                        [
                            dcc.Loading(
                                id="loading-time",
                                type="default",
                                children=[
                                    dcc.Graph(
                                        id="time-domain-plot",
                                        style={"marginBottom": "0"},
                                        config={"responsive": True},
                                    )
                                ],
                            )
                        ],
                        className="p-0",
                    ),
                ],
                className="mb-3",
            ),
            
            # Frequency Domain Plot
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H6("📊 Frequency Spectrum (FFT)", className="mb-0")
                    ),
                    dbc.CardBody(
                        [
                            dcc.Loading(
                                id="loading-freq",
                                type="default",
                                children=[
                                    dcc.Graph(
                                        id="frequency-domain-plot",
                                        style={"marginBottom": "0"},
                                        config={"responsive": True},
                                    )
                                ],
                            )
                        ],
                        className="p-0",
                    ),
                ],
                className="mb-3",
            ),
            
            # Phase and PSD Plots Row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            "Phase Spectrum",
                                            className="mb-0",
                                        )
                                    ),
                                    dbc.CardBody(
                                        [
                                            dcc.Loading(
                                                id="loading-phase",
                                                type="default",
                                                children=[
                                                    dcc.Graph(
                                                        id="phase-plot",
                                                        style={"marginBottom": "0"},
                                                        config={"responsive": True},
                                                    )
                                                ],
                                            )
                                        ],
                                        className="p-0",
                                    ),
                                ]
                            )
                        ],
                        width=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6("Power Spectral Density", className="mb-0")
                                    ),
                                    dbc.CardBody(
                                        [
                                            dcc.Loading(
                                                id="loading-psd",
                                                type="default",
                                                children=[
                                                    dcc.Graph(
                                                        id="psd-plot",
                                                        style={"marginBottom": "0"},
                                                        config={"responsive": True},
                                                    )
                                                ],
                                            )
                                        ],
                                        className="p-0",
                                    ),
                                ]
                            )
                        ],
                        width=6,
                        className="mb-3",
                    ),
                ],
            ),
            
            # Comparison Plot (Raw vs Filtered)
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H6("Raw vs Filtered Signal Comparison", className="mb-0")
                    ),
                    dbc.CardBody(
                        [
                            dcc.Loading(
                                id="loading-comparison",
                                type="default",
                                children=[
                                    dcc.Graph(
                                        id="comparison-plot",
                                        style={"marginBottom": "0"},
                                        config={"responsive": True},
                                    )
                                ],
                            )
                        ],
                        className="p-0",
                    ),
                ],
                className="mb-3",
            ),
        ],
        width=9,
        className="p-3",
        style={"overflowY": "auto", "maxHeight": "100vh"},
    )
