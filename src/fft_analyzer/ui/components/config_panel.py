"""
Configuration panel component for Dash UI.

Provides controls for signal generation, filter settings, and analysis parameters.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_config_panel() -> dbc.Col:
    """
    Create the left configuration panel with signal controls.

    Returns:
        dbc.Col: Bootstrap column containing configuration controls
    """
    return dbc.Col(
        [
            html.H4("Configuration Panel", className="mb-4"),
            
            # Signal Source Section
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Signal Source", className="mb-0")),
                    dbc.CardBody(
                        [
                            dbc.RadioItems(
                                id="signal-source-radio",
                                options=[
                                    {"label": " Generate Signal", "value": "generate"},
                                    {"label": " Import from File", "value": "import"},
                                ],
                                value="generate",
                                inline=False,
                                className="mb-3",
                            ),
                            dcc.Upload(
                                id="signal-file-upload",
                                children=html.Div(
                                    ["Drag and Drop or ", html.A("Select Files")],
                                    className="text-center",
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px 0",
                                },
                                multiple=False,
                            ),
                            html.Div(id="file-upload-status", className="text-muted small mt-2"),
                        ]
                    ),
                ],
                className="mb-3",
            ),
            
            # Signal Parameters Section
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Signal Parameters", className="mb-0")),
                    dbc.CardBody(
                        [
                            html.Label("Frequency Component 1 (Hz):", className="fw-bold"),
                            dcc.Input(
                                id="freq1-input",
                                type="number",
                                value=50,
                                step=1,
                                min=0,
                                className="form-control mb-2",
                            ),
                            html.Label("Frequency Component 2 (Hz):", className="fw-bold"),
                            dcc.Input(
                                id="freq2-input",
                                type="number",
                                value=120,
                                step=1,
                                min=0,
                                className="form-control mb-2",
                            ),
                            html.Label("Amplitude 1:", className="fw-bold"),
                            dcc.Slider(
                                id="amp1-slider",
                                min=0,
                                max=2,
                                step=0.1,
                                value=1.0,
                                marks={0: "0", 1: "1", 2: "2"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Div(className="mb-2"),
                            html.Label("Amplitude 2:", className="fw-bold"),
                            dcc.Slider(
                                id="amp2-slider",
                                min=0,
                                max=2,
                                step=0.1,
                                value=0.5,
                                marks={0: "0", 1: "1", 2: "2"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Div(className="mb-2"),
                            html.Label("Noise SNR (dB):", className="fw-bold"),
                            dcc.Slider(
                                id="snr-slider",
                                min=0,
                                max=100,
                                step=5,
                                value=20,
                                marks={0: "0", 50: "50", 100: "100"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Div(className="mb-2"),
                            html.Label("Sampling Rate (Hz):", className="fw-bold"),
                            dcc.Input(
                                id="fs-input",
                                type="number",
                                value=1000,
                                step=100,
                                min=100,
                                className="form-control mb-2",
                            ),
                            html.Label("Duration (seconds):", className="fw-bold"),
                            dcc.Input(
                                id="duration-input",
                                type="number",
                                value=1.0,
                                step=0.1,
                                min=0.1,
                                className="form-control",
                            ),
                        ]
                    ),
                ],
                className="mb-3",
            ),
            
            # Filter Settings Section
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Filter Settings", className="mb-0")),
                    dbc.CardBody(
                        [
                            html.Label("Filter Type:", className="fw-bold"),
                            dcc.Dropdown(
                                id="filter-type-dropdown",
                                options=[
                                    {"label": "None", "value": "none"},
                                    {"label": "Low-Pass", "value": "lowpass"},
                                    {"label": "High-Pass", "value": "highpass"},
                                    {"label": "Band-Pass", "value": "bandpass"},
                                    {"label": "Notch", "value": "notch"},
                                ],
                                value="none",
                                className="mb-2",
                            ),
                            html.Label("Cutoff Frequency (Hz):", className="fw-bold"),
                            dcc.Input(
                                id="cutoff-input",
                                type="number",
                                value=200,
                                step=10,
                                min=0,
                                className="form-control mb-2",
                            ),
                            html.Label("Filter Order:", className="fw-bold"),
                            dcc.Slider(
                                id="filter-order-slider",
                                min=1,
                                max=8,
                                step=1,
                                value=4,
                                marks={1: "1", 4: "4", 8: "8"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ]
                    ),
                ],
                className="mb-3",
            ),
            
            # Window Function Section
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("FFT Settings", className="mb-0")),
                    dbc.CardBody(
                        [
                            html.Label("Window Function:", className="fw-bold"),
                            dcc.Dropdown(
                                id="window-dropdown",
                                options=[
                                    {"label": "Hann", "value": "hann"},
                                    {"label": "Hamming", "value": "hamming"},
                                    {"label": "Blackman", "value": "blackman"},
                                    {"label": "Rectangle", "value": "rectangle"},
                                ],
                                value="hann",
                                className="mb-2",
                            ),
                            dbc.Checklist(
                                id="zero-pad-checkbox",
                                options=[
                                    {"label": " Enable Zero Padding", "value": 1}
                                ],
                                value=[1],
                                className="mb-2",
                            ),
                            html.Label("Peak Detection Threshold:", className="fw-bold"),
                            dcc.Slider(
                                id="peak-threshold-slider",
                                min=0,
                                max=1,
                                step=0.05,
                                value=0.1,
                                marks={0: "0%", 0.5: "50%", 1: "100%"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ]
                    ),
                ],
                className="mb-3",
            ),
            
            # Action Buttons
            dbc.Card(
                [
                    html.Button(
                        "▶ ANALYZE",
                        id="analyze-button",
                        n_clicks=0,
                        className="btn btn-primary w-100 mb-2",
                        style={"fontSize": "16px", "padding": "12px"},
                    ),
                    html.Button(
                        "⬇ EXPORT",
                        id="export-button",
                        n_clicks=0,
                        className="btn btn-secondary w-100",
                        style={"fontSize": "16px", "padding": "12px"},
                    ),
                ],
                className="mt-3",
            ),
        ],
        width=3,
        className="p-3 bg-light",
        style={"maxHeight": "100vh", "overflowY": "auto"},
    )
