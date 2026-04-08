"""
Peaks table component for Dash UI.

Displays detected frequency peaks in a formatted table.
"""

from typing import List
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd

from fft_analyzer.models.peak_info import PeakInfo


def create_peaks_table(peaks: List[PeakInfo] = None) -> dbc.Card:
    """
    Create a table displaying detected frequency peaks.

    Args:
        peaks: List of PeakInfo objects to display

    Returns:
        dbc.Card: Bootstrap card containing peaks table
    """
    if peaks is None or len(peaks) == 0:
        data = [{
            "Index": "-",
            "Frequency (Hz)": "-",
            "Magnitude": "-",
            "Magnitude (dB)": "-",
            "Prominence": "-",
        }]
    else:
        data = [
            {
                "Index": i + 1,
                "Frequency (Hz)": f"{peak.frequency:.2f}",
                "Magnitude": f"{peak.magnitude:.6f}",
                "Magnitude (dB)": f"{peak.magnitude_db:.2f}",
                "Prominence": f"{peak.prominence:.6f}",
            }
            for i, peak in enumerate(peaks[:20])  # Show top 20 peaks
        ]

    df = pd.DataFrame(data)

    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5("🎯 Detected Frequency Peaks", className="mb-0"),
            ),
            dbc.CardBody(
                [
                    html.Div(
                        id="peaks-table-container",
                        children=[
                            dash_table.DataTable(
                                id="peaks-data-table",
                                columns=[
                                    {"name": "Index", "id": "Index"},
                                    {"name": "Frequency (Hz)", "id": "Frequency (Hz)"},
                                    {"name": "Magnitude", "id": "Magnitude"},
                                    {"name": "Magnitude (dB)", "id": "Magnitude (dB)"},
                                    {"name": "Prominence", "id": "Prominence"},
                                ],
                                data=data,
                                style_cell={
                                    "textAlign": "center",
                                    "padding": "10px",
                                    "fontFamily": "monospace",
                                    "fontSize": "13px",
                                },
                                style_header={
                                    "backgroundColor": "#e9ecef",
                                    "fontWeight": "bold",
                                    "borderBottom": "2px solid #dee2e6",
                                },
                                style_data={
                                    "borderBottom": "1px solid #dee2e6",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": "#f8f9fa",
                                    }
                                ],
                                page_size=10,
                                style_table={
                                    "overflowX": "auto",
                                    "width": "100%",
                                },
                            )
                        ],
                    ),
                    html.Div(
                        id="peaks-summary",
                        className="mt-3 text-muted small",
                        children="No peaks detected yet. Run analysis to detect frequency peaks.",
                    ),
                ],
                className="p-3",
            ),
        ],
        className="mt-4",
    )


def update_peaks_table(peaks: List[PeakInfo] = None) -> tuple:
    """
    Update peaks table data and summary.

    Args:
        peaks: List of PeakInfo objects

    Returns:
        Tuple of (table_data, summary_text)
    """
    if peaks is None or len(peaks) == 0:
        data = [{
            "Index": "-",
            "Frequency (Hz)": "-",
            "Magnitude": "-",
            "Magnitude (dB)": "-",
            "Prominence": "-",
        }]
        summary = "No peaks detected yet."
    else:
        data = [
            {
                "Index": i + 1,
                "Frequency (Hz)": f"{peak.frequency:.2f}",
                "Magnitude": f"{peak.magnitude:.6f}",
                "Magnitude (dB)": f"{peak.magnitude_db:.2f}",
                "Prominence": f"{peak.prominence:.6f}",
            }
            for i, peak in enumerate(peaks[:20])
        ]
        summary = f"Detected {len(peaks)} peaks (showing top 20)"

    return data, summary
