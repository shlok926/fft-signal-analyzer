"""Dash layout definition for FFT Signal Analyzer."""

from dash import dcc, html
import dash_bootstrap_components as dbc


def create_layout():
    """Create main layout for the Dash dashboard.
    
    Returns:
        Dash layout HTML structure.
    """
    return dbc.Container(
        [
            # Header
            dbc.Row(
                [
                    dbc.Col(
                        html.H1(
                            "🔷 FFT Signal Analyzer",
                            className="text-primary mb-4",
                        ),
                        width=9,
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Export Analysis",
                                id="btn-export",
                                color="success",
                                size="sm",
                                className="me-2",
                            ),
                            dbc.Button(
                                "Settings",
                                id="btn-settings",
                                color="secondary",
                                size="sm",
                            ),
                        ],
                        width=3,
                        className="text-end",
                    ),
                ],
                className="mb-4",
            ),

            # Main container
            dbc.Row(
                [
                    # Left panel: Configuration
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H5("Configuration")),
                                    dbc.CardBody(
                                        [
                                            # Signal source
                                            html.Label(
                                                "Signal Source:",
                                                className="fw-bold",
                                            ),
                                            dcc.RadioItems(
                                                id="radio-signal-source",
                                                options=[
                                                    {"label": " Generate", "value": "generate"},
                                                    {"label": " Import File", "value": "import"},
                                                ],
                                                value="generate",
                                                inline=True,
                                                className="mb-3",
                                            ),

                                            # Import file upload (hidden by default)
                                            html.Div(
                                                id="div-import-file",
                                                style={"display": "none"},
                                                children=[
                                                    dcc.Upload(
                                                        id="signal-file-upload",
                                                        children=html.Div(
                                                            [
                                                                "📁 Drag & Drop or ",
                                                                html.A("Select CSV File"),
                                                            ]
                                                        ),
                                                        style={
                                                            "width": "100%",
                                                            "height": "60px",
                                                            "lineHeight": "60px",
                                                            "borderWidth": "2px",
                                                            "borderStyle": "dashed",
                                                            "borderRadius": "5px",
                                                            "textAlign": "center",
                                                            "margin": "10px 0",
                                                        },
                                                        multiple=False,
                                                    ),
                                                    html.Div(
                                                        id="file-upload-status",
                                                        className="text-muted small mt-2",
                                                    ),
                                                ],
                                            ),

                                            # Generate signal parameters
                                            html.Div(
                                                id="div-generate-params",
                                                children=[
                                                    html.Label(
                                                        "Generator Parameters:",
                                                        className="fw-bold mt-3",
                                                    ),
                                                    html.Label("Frequency 1 (Hz):"),
                                                    dcc.Input(
                                                        id="input-freq1",
                                                        type="number",
                                                        value=50,
                                                        min=0,
                                                        step=1,
                                                        className="form-control",
                                                    ),
                                                    html.Label("Amplitude 1:", className="mt-2"),
                                                    dcc.Input(
                                                        id="input-amp1",
                                                        type="number",
                                                        value=1.0,
                                                        min=0,
                                                        step=0.1,
                                                        className="form-control",
                                                    ),
                                                    html.Label("Frequency 2 (Hz):", className="mt-2"),
                                                    dcc.Input(
                                                        id="input-freq2",
                                                        type="number",
                                                        value=120,
                                                        min=0,
                                                        step=1,
                                                        className="form-control",
                                                    ),
                                                    html.Label("Amplitude 2:", className="mt-2"),
                                                    dcc.Input(
                                                        id="input-amp2",
                                                        type="number",
                                                        value=0.5,
                                                        min=0,
                                                        step=0.1,
                                                        className="form-control",
                                                    ),
                                                    html.Label("Noise (SNR dB):", className="mt-2"),
                                                    dcc.Input(
                                                        id="input-snr",
                                                        type="number",
                                                        value=20,
                                                        min=0,
                                                        step=1,
                                                        className="form-control",
                                                    ),
                                                    html.Label(
                                                        "Sampling Rate (Hz):",
                                                        className="mt-2",
                                                    ),
                                                    dcc.Input(
                                                        id="input-fs",
                                                        type="number",
                                                        value=1000,
                                                        min=1,
                                                        step=10,
                                                        className="form-control",
                                                    ),
                                                    html.Label("Duration (s):", className="mt-2"),
                                                    dcc.Input(
                                                        id="input-duration",
                                                        type="number",
                                                        value=1.0,
                                                        min=0.1,
                                                        step=0.1,
                                                        className="form-control",
                                                    ),
                                                ],
                                            ),

                                            # Filter settings
                                            html.Label(
                                                "Filter Settings:",
                                                className="fw-bold mt-3",
                                            ),
                                            html.Label("Window Function:"),
                                            dcc.Dropdown(
                                                id="dropdown-window",
                                                options=[
                                                    {"label": "Hann", "value": "hann"},
                                                    {"label": "Hamming", "value": "hamming"},
                                                    {"label": "Blackman", "value": "blackman"},
                                                    {"label": "Rectangle", "value": "rectangle"},
                                                ],
                                                value="hann",
                                                className="form-control",
                                            ),
                                            html.Label("Filter Type:", className="mt-2"),
                                            dcc.Dropdown(
                                                id="dropdown-filter-type",
                                                options=[
                                                    {"label": "None", "value": "none"},
                                                    {"label": "Low-Pass", "value": "lowpass"},
                                                    {"label": "High-Pass", "value": "highpass"},
                                                    {"label": "Band-Pass", "value": "bandpass"},
                                                    {"label": "Notch", "value": "notch"},
                                                ],
                                                value="none",
                                                className="form-control",
                                            ),
                                            html.Label("Cutoff Frequency (Hz):", className="mt-2"),
                                            dcc.Input(
                                                id="input-cutoff",
                                                type="number",
                                                value=200,
                                                min=0,
                                                step=10,
                                                className="form-control",
                                            ),

                                            # Action buttons
                                            html.Div(
                                                [
                                                    dbc.Button(
                                                        "▶ Analyze",
                                                        id="btn-analyze",
                                                        color="primary",
                                                        size="lg",
                                                        className="w-100 mt-4",
                                                    ),
                                                    html.Div(
                                                        id="file-download-status",
                                                        className="text-success mt-2 small",
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3",
                            ),
                        ],
                        width=12,
                        lg=3,
                    ),

                    # Right panel: Plots
                    dbc.Col(
                        [
                            # Time domain plot
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H5("📈 Time Domain Signal")),
                                    dbc.CardBody(
                                        dcc.Loading(
                                            id="loading-time-plot",
                                            type="default",
                                            children=dcc.Graph(id="graph-time-domain"),
                                        )
                                    ),
                                ],
                                className="mb-3",
                            ),

                            # Frequency domain plot
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H5("📊 Frequency Spectrum")),
                                    dbc.CardBody(
                                        dcc.Loading(
                                            id="loading-freq-plot",
                                            type="default",
                                            children=dcc.Graph(id="graph-freq-domain"),
                                        )
                                    ),
                                ],
                                className="mb-3",
                            ),

                            # Phase and PSD plots
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(html.H6("Phase Spectrum")),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="graph-phase"),
                                                    ),
                                                ],
                                            ),
                                        ],
                                        width=12,
                                        lg=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(html.H6("Power Spectral Density")),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="graph-psd"),
                                                    ),
                                                ],
                                            ),
                                        ],
                                        width=12,
                                        lg=6,
                                    ),
                                ],
                                className="mb-3",
                            ),

                            # Peaks table
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H5("Detected Peaks")),
                                    dbc.CardBody(
                                        dcc.Loading(
                                            id="loading-peaks-table",
                                            type="default",
                                            children=html.Div(
                                                id="div-peaks-table",
                                                style={"overflowX": "auto"},
                                            ),
                                        )
                                    ),
                                ],
                            ),
                        ],
                        width=12,
                        lg=9,
                    ),
                ],
                className="g-3",
            ),

            # Settings Modal
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("⚙️ Settings")),
                    dbc.ModalBody(
                        [
                            html.Label("Peak Detection Threshold (0-1):", className="fw-bold"),
                            dcc.Slider(
                                id="settings-peak-threshold",
                                min=0,
                                max=1,
                                step=0.05,
                                value=0.1,
                                marks={0: "0", 0.5: "0.5", 1: "1"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Div(className="mb-3"),
                            html.Label("FFT Zero Padding:", className="fw-bold mt-2"),
                            dcc.Checklist(
                                id="settings-zero-pad",
                                options=[{"label": " Enable Zero Padding", "value": 1}],
                                value=[1],
                            ),
                            html.Div(className="mb-3"),
                            html.Label("Export Format:", className="fw-bold mt-2"),
                            dcc.Dropdown(
                                id="settings-export-format",
                                options=[
                                    {"label": "CSV", "value": "csv"},
                                    {"label": "PNG", "value": "png"},
                                    {"label": "PDF", "value": "pdf"},
                                ],
                                value="csv",
                            ),
                            html.Div(className="mb-2"),
                            html.P(
                                "⚙️ Settings are saved and applied to next analysis",
                                className="text-muted small mt-3",
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button("Close", id="settings-close", color="secondary"),
                            dbc.Button("Save", id="settings-save", color="primary", className="ms-2"),
                        ]
                    ),
                ],
                id="modal-settings",
                is_open=False,
                size="lg",
            ),

            # Hidden div to store signal data
            dcc.Store(id="store-signal-data"),
            dcc.Store(id="store-spectrum-data"),
            dcc.Store(id="store-peaks-data"),
            dcc.Store(id="store-settings"),
        ],
        fluid=True,
        className="py-4",
    )
