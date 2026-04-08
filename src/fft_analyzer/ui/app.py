"""Dash application factory and setup."""

import dash
from dash import dcc, html, State
from .layout import create_layout
from .callbacks import register_callbacks
from ..utils import logger


def create_app(debug: bool = False):
    """Create and configure Dash application.
    
    Args:
        debug: Whether to run in debug mode.
        
    Returns:
        Configured Dash app instance.
    """
    # Create Dash app
    app = dash.Dash(
        __name__,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )

    # Set title
    app.title = "FFT Signal Analyzer"

    # Create layout
    app.layout = create_layout()

    # Register callbacks
    register_callbacks(app)

    logger.info("Dash app created successfully")

    return app


if __name__ == "__main__":
    app = create_app(debug=True)
    logger.info("Starting Dash server at http://127.0.0.1:8050/")
    app.run(debug=True, host="127.0.0.1", port=8050)
