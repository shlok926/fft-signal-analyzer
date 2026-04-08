"""
AI-Enhanced Spectrum Analyzer - Professional Streamlit Dashboard
Real-Time Signal Processing and Frequency Analysis
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
from pathlib import Path
import io
import json
import time

# Production-grade imports
try:
    from src.fft_analyzer.utils import (
        get_logger, get_config, safe_execute,
        SessionManager, CacheManager, ErrorHandler
    )
    logger = get_logger("streamlit_app")
    config = get_config
    session_mgr = SessionManager()
    cache_mgr = CacheManager()
except ImportError:
    logger = None
    config = lambda x, default=None: default
    session_mgr = None
    cache_mgr = None

# Import export manager
try:
    from src.fft_analyzer.export.export_manager import ExportManager, generate_export_report
except ImportError:
    ExportManager = None
    generate_export_report = None

if logger:
    logger.info("=" * 60)
    logger.info("AI-Enhanced Spectrum Analyzer Started")
    logger.info("=" * 60)

# ============================================================================
# PAGE CONFIG & THEME SETUP
# ============================================================================
st.set_page_config(
    page_title="AI Spectrum Analyzer",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark theme with neon accents
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary-color: #00D4FF;      /* Neon Blue */
        --secondary-color: #39FF14;    /* Neon Green */
        --accent-color: #FF006E;       /* Hot Pink */
        --background: #0A0E27;         /* Dark Background */
        --surface: #1A1F3A;            /* Surface */
        --text-primary: #FFFFFF;       /* White */
        --text-secondary: #B0B9C6;     /* Light Grey */
    }
    
    /* Background */
    body {
        background-color: #0A0E27;
        color: #FFFFFF;
    }
    
    .main {
        background-color: #0A0E27;
        color: #FFFFFF;
    }
    
    .stApp {
        background-color: #0A0E27;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1A1F3A;
        border-right: 2px solid #00D4FF;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #1A1F3A;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1A1F3A 0%, #2A3555 100%);
        border-left: 4px solid #00D4FF;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00D4FF;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #00D4FF;
        color: #0A0E27;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #39FF14;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.5);
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background-color: #00D4FF;
    }
    
    /* Dividers */
    hr {
        border-color: #00D4FF;
        opacity: 0.3;
    }
    
    /* Cards/Containers */
    .stSelectbox > div > div,
    .stNumberInput > div > div {
        background-color: #1A1F3A;
        border: 1px solid #00D4FF;
        border-radius: 4px;
    }
    
    /* Text colors */
    .stMarkdown {
        color: #FFFFFF;
    }
    
    .help-text {
        color: #B0B9C6;
        font-size: 12px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_signal_generator():
    """Import signal generator (cached)"""
    from src.fft_analyzer.core import SignalGenerator
    return SignalGenerator

@st.cache_resource
def get_fft_engine():
    """Import FFT engine (cached)"""
    from src.fft_analyzer.core import FFTEngine
    return FFTEngine

@st.cache_resource
def get_filter_engine():
    """Import filter engine (cached)"""
    from src.fft_analyzer.core import FilterEngine
    return FilterEngine

@st.cache_resource
def get_peak_detector():
    """Import peak detector (cached)"""
    from src.fft_analyzer.core import PeakDetector
    return PeakDetector

@st.cache_resource
def get_signal_data():
    """Import SignalData model (cached)"""
    from src.fft_analyzer.models import SignalData
    return SignalData

def create_all_plots(signal, spectrum, peaks):
    """Create all 4 plots for the dashboard"""
    
    # Time-Domain Plot
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=signal.time,
        y=signal.amplitude,
        mode='lines',
        name='Signal',
        line=dict(color='#00D4FF', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)'
    ))
    
    fig_time.update_layout(
        height=400,
        template="plotly_dark",
        paper_bgcolor="#0A0E27",
        plot_bgcolor="#1A1F3A",
        font=dict(color="#FFFFFF", family="Arial"),
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=30),
        showlegend=True,
        title="📈 Time-Domain Signal"
    )
    
    # Frequency Spectrum Plot
    fig_freq = go.Figure()
    fig_freq.add_trace(go.Scatter(
        x=spectrum.freqs,
        y=spectrum.magnitude,
        mode='lines',
        name='Spectrum',
        line=dict(color='#39FF14', width=2),
    ))
    
    if peaks:
        peak_freqs = [p.frequency for p in peaks]
        peak_mags = [p.magnitude for p in peaks]
        
        fig_freq.add_trace(go.Scatter(
            x=peak_freqs,
            y=peak_mags,
            mode='markers+text',
            name='Detected Peaks',
            marker=dict(size=10, color='#FF006E', symbol='star'),
            text=[f"{p.frequency:.1f} Hz" for p in peaks],
            textposition="top center",
            textfont=dict(color='#FF006E', size=10),
        ))
    
    fig_freq.update_layout(
        height=400,
        template="plotly_dark",
        paper_bgcolor="#0A0E27",
        plot_bgcolor="#1A1F3A",
        font=dict(color="#FFFFFF", family="Arial"),
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=30),
        showlegend=True,
        title="📊 Frequency Spectrum (FFT)"
    )
    
    # Phase Spectrum Plot
    fig_phase = go.Figure()
    fig_phase.add_trace(go.Scatter(
        x=spectrum.freqs,
        y=spectrum.phase,
        mode='lines',
        name='Phase',
        line=dict(color='#FF006E', width=2),
    ))
    
    fig_phase.update_layout(
        height=300,
        template="plotly_dark",
        paper_bgcolor="#0A0E27",
        plot_bgcolor="#1A1F3A",
        font=dict(color="#FFFFFF", family="Arial"),
        xaxis_title="Frequency (Hz)",
        yaxis_title="Phase (radians)",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=30),
        title="🔍 Phase Spectrum"
    )
    
    # PSD Plot
    fig_psd = go.Figure()
    fig_psd.add_trace(go.Scatter(
        x=spectrum.freqs,
        y=spectrum.psd,
        mode='lines',
        name='PSD',
        fill='tozeroy',
        line=dict(color='#00D4FF', width=2),
        fillcolor='rgba(0, 212, 255, 0.2)',
    ))
    
    fig_psd.update_layout(
        height=300,
        template="plotly_dark",
        paper_bgcolor="#0A0E27",
        plot_bgcolor="#1A1F3A",
        font=dict(color="#FFFFFF", family="Arial"),
        xaxis_title="Frequency (Hz)",
        yaxis_title="Power (V²/Hz)",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=30),
        title="⚡ Power Spectral Density"
    )
    
    return fig_time, fig_freq, fig_phase, fig_psd

def create_metric_card(title, value, unit="", color="#00D4FF"):
    """Create a metric card with styled HTML"""
    return f"""
    <div class="metric-card" style="border-left-color: {color};">
        <div style="color: #B0B9C6; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
            {title}
        </div>
        <div style="color: {color}; font-size: 28px; font-weight: bold; margin-top: 8px;">
            {value} <span style="font-size: 16px;">{unit}</span>
        </div>
    </div>
    """

# ============================================================================
# HEADER SECTION
# ============================================================================

col1, col2 = st.columns([8, 2])

with col1:
    st.markdown("""
    <h1 style="margin: 0; font-size: 40px;">📡 AI-Enhanced Spectrum Analyzer</h1>
    <p style="color: #B0B9C6; margin-top: 5px; font-size: 14px; letter-spacing: 1px;">
        Real-Time Signal Processing → Frequency Domain Analysis → Intelligent Filtering
    </p>
    """, unsafe_allow_html=True)

with col2:
    status = st.metric(
        "System Status",
        "🟢 ACTIVE",
        "Ready",
        delta_color="off"
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONTROL PANEL
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ CONTROL PANEL")
    st.markdown("<div class='help-text'>Configure signal parameters and analysis settings</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ====================================================================
    # SIGNAL SOURCE SELECTION - GENERATE vs IMPORT
    # ====================================================================
    tab_generate, tab_import = st.tabs(["📊 Generate Signal", "📁 Import File"])
    
    with tab_generate:
        st.markdown("**Generate Signal Manually**")
        
        # Signal Generation Section
        st.markdown("📋 **Signal Configuration**")
        
        freq1 = st.slider(
            "Frequency 1 (Hz)",
            0, 5000, 50,
            help="Set first frequency component (0-5000 Hz)",
            key="freq1_gen"
        )
        
        amp1 = st.slider(
            "Amplitude 1",
            0.0, 10.0, 1.0, 0.1,
            help="Amplitude of first component (0.0-10.0)",
            key="amp1_gen"
        )
        
        freq2 = st.slider(
            "Frequency 2 (Hz)",
            0, 5000, 120,
            help="Set second frequency component (0-5000 Hz)",
            key="freq2_gen"
        )
        
        amp2 = st.slider(
            "Amplitude 2",
            0.0, 10.0, 0.5, 0.1,
            help="Amplitude of second component (0.0-10.0)",
            key="amp2_gen"
        )
        
        # Noise Section
        st.markdown("🔊 **Noise Parameters**")
        
        snr_db = st.slider(
            "Noise Level (SNR dB)",
            0, 100, 20, 5,
            help="Signal-to-Noise Ratio in dB (lower = more noise)",
            key="snr_gen"
        )
        
        # Sampling Section
        st.markdown("⏱️ **Sampling Parameters**")
        
        fs = st.number_input(
            "Sampling Rate (Hz)",
            10, 100000, 1000, 100,
            help="Samples per second (10-100,000 Hz)",
            key="fs_gen"
        )
        
        generate_mode = True
        imported_file = None
        
    with tab_import:
        st.markdown("**Import Signal from File**")
        st.info("✅ Supported formats: `.csv`, `.wav`, `.npy`")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a signal file:",
            type=["csv", "wav", "npy"],
            help="Upload CSV (1 or 2 columns), WAV (audio), or NPY (NumPy) files"
        )
        
        if uploaded_file:
            file_ext = Path(uploaded_file.name).suffix.lower()
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # For CSV and NPY, ask for sampling rate
            if file_ext in ['.csv', '.npy']:
                fs_import = st.number_input(
                    "Sampling Rate (Hz) for imported file:",
                    10, 100000, 1000, 100,
                    help="Used to calculate time axis (10-100,000 Hz)",
                    key="fs_import"
                )
            else:
                fs_import = None  # WAV files have built-in fs
            
            # Load the file
            try:
                import tempfile
                from src.fft_analyzer.core import SignalLoader
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                # Load based on file type
                if file_ext == '.csv':
                    signal_imported = SignalLoader.load_csv(tmp_path, fs=fs_import)
                    st.success(f"✅ CSV loaded: {len(signal_imported.amplitude)} samples")
                    
                elif file_ext == '.wav':
                    signal_imported = SignalLoader.load_wav(tmp_path)
                    st.success(f"✅ WAV loaded: fs={signal_imported.fs} Hz, {len(signal_imported.amplitude)} samples")
                    
                elif file_ext == '.npy':
                    signal_imported = SignalLoader.load_npy(tmp_path, fs=fs_import)
                    st.success(f"✅ NPY loaded: {len(signal_imported.amplitude)} samples")
                
                # Store in session state
                st.session_state.imported_signal = signal_imported
                imported_file = uploaded_file.name
                generate_mode = False
                
                # Show signal info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Duration", f"{signal_imported.duration:.2f}s")
                with col2:
                    st.metric("Samples", len(signal_imported.amplitude))
                with col3:
                    st.metric("Sampling Rate", f"{signal_imported.fs:.0f} Hz")
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                generate_mode = True
                imported_file = None
        else:
            generate_mode = True
            imported_file = None
            if 'imported_signal' in st.session_state:
                del st.session_state.imported_signal
    
    st.markdown("---")
    
    # ====================================================================
    # FFT & FILTER PARAMETERS (Common to both modes)
    # ====================================================================
    
    if not generate_mode or imported_file:
        fs = fs_import if imported_file else fs
    
    duration = st.number_input(
        "Duration (seconds)",
        0.01, 100.0, 1.0, 0.1,
        help="Signal duration in seconds (0.01-100 sec)"
    )
    
    st.markdown("---")
    
    # Initialize filter variables
    cutoff_freq = None
    cutoff_freq_high = None
    
    # FFT Settings
    with st.expander("🔍 **FFT Settings**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            window_type = st.selectbox(
                "Window Function",
                ["hann", "hamming", "blackman", "rectangle", "bartlett", "kaiser"],
                help="Window reduces spectral leakage. Hann is default, Kaiser for high dynamic range",
                key="win_func"
            )
        
        with col2:
            zero_pad = st.checkbox(
                "Zero Padding",
                value=True,
                help="✅ Improves frequency resolution (recommended)"
            )
        
        # Info box
        if window_type == "hann":
            st.info("🎵 **Hann Window**: Excellent general-purpose window, good spectral leakage control")
        elif window_type == "kaiser":
            st.info("🎵 **Kaiser Window**: Best for high dynamic range signals, adjustable sidelobe level")
        elif window_type == "blackman":
            st.info("🎵 **Blackman Window**: Excellent sidelobe suppression, wider main lobe")
    
    st.markdown("---")
    
    # Digital Filter Settings
    with st.expander("🔻 **Digital Filter**", expanded=False):
        filter_type = st.selectbox(
            "Filter Type",
            [
                "None",
                "Low-Pass (Remove high frequencies)",
                "High-Pass (Remove low frequencies)",
                "Band-Pass (Keep frequency range)",
                "Notch (Remove specific frequency)",
            ],
            help="Select filter type for signal preprocessing",
            key="filt_type"
        )
        
        if filter_type != "None":
            if "Band-Pass" in filter_type:
                col1, col2 = st.columns(2)
                with col1:
                    cutoff_freq = st.number_input(
                        "Low Cutoff (Hz)",
                        1, int(fs/2)-1, 50,
                        key="cutoff_low"
                    )
                with col2:
                    cutoff_freq_high = st.number_input(
                        "High Cutoff (Hz)",
                        int(cutoff_freq)+1, int(fs/2), 200,
                        key="cutoff_high"
                    )
            else:
                cutoff_freq = st.slider(
                    "Cutoff Frequency (Hz)",
                    1, int(fs/2)-1, 200,
                    key="cutoff_freq"
                )
                st.info(f"📍 Filter will apply at: {cutoff_freq} Hz")
        else:
            cutoff_freq = None
            cutoff_freq_high = None
    
    st.markdown("---")
    
    # Action Buttons with enhanced styling
    st.markdown("<h4 style='color: #00D4FF;'>Actions</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analyze_button = st.button(
            "▶️ ANALYZE",
            width='stretch',
            key="analyze"
        )
    
    with col2:
        export_button = st.button(
            "⬇️ EXPORT",
            width='stretch',
            key="export"
        )
    
    with col3:
        reset_button = st.button(
            "🔄 RESET",
            width='stretch',
            key="reset",
            help="Clear all analysis and start over"
        )
        
        if reset_button:
            st.session_state.analysis_data = None
            st.session_state.compression_result = None
            st.session_state.anomaly_result = None
            st.session_state.classification_result = None
            st.rerun()

# ============================================================================
# ANALYSIS LOGIC
# ============================================================================

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if analyze_button:
    start_time = time.time()
    
    with st.spinner("🔄 Analyzing signal..."):
        try:
            # Log analysis start
            if logger:
                logger.info("Analysis started - Mode: " + ("Import" if 'imported_signal' in st.session_state else "Generate"))
            
            # Import modules
            SignalGenerator = get_signal_generator()
            FFTEngine = get_fft_engine()
            FilterEngine = get_filter_engine()
            PeakDetector = get_peak_detector()
            SignalData = get_signal_data()
            
            # Generate or use imported signal
            if 'imported_signal' in st.session_state and st.session_state.imported_signal is not None:
                signal_data = st.session_state.imported_signal
                msg = f"Using imported signal: {signal_data.label} ({len(signal_data.amplitude)} samples @ {signal_data.fs} Hz)"
                if logger:
                    logger.info("OK: " + msg)
                print(f"\n✅ {msg}")
            else:
                # Generate signal manually
                components = [
                    {"frequency": freq1, "amplitude": amp1, "phase": 0},
                    {"frequency": freq2, "amplitude": amp2, "phase": 0},
                ]
                
                signal_data = SignalGenerator.generate_signal(
                    components=components,
                    fs=fs,
                    duration=duration,
                    snr_db=snr_db,
                    label="Generated Signal"
                )
                msg = f"Generated signal with {len(signal_data.amplitude)} samples"
                if logger:
                    logger.info("OK: " + msg)
                print(f"\n✅ {msg}")
            
            # Apply filter
            filtered_signal = signal_data
            if filter_type != "None":
                # Extract filter type from description string
                if "Low-Pass" in filter_type:
                    filtered_signal = FilterEngine.low_pass(signal_data, cutoff_freq)
                    if logger:
                        logger.info(f"OK: Applied Low-Pass filter at {cutoff_freq} Hz")
                elif "High-Pass" in filter_type:
                    filtered_signal = FilterEngine.high_pass(signal_data, cutoff_freq)
                    if logger:
                        logger.info(f"OK: Applied High-Pass filter at {cutoff_freq} Hz")
                elif "Band-Pass" in filter_type:
                    filtered_signal = FilterEngine.low_pass(signal_data, cutoff_freq_high)
                    filtered_signal = FilterEngine.high_pass(filtered_signal, cutoff_freq)
                    if logger:
                        logger.info(f"OK: Applied Band-Pass filter {cutoff_freq}-{cutoff_freq_high} Hz")
                elif "Notch" in filter_type:
                    filtered_signal = FilterEngine.low_pass(signal_data, cutoff_freq * 0.95)
                    filtered_signal = FilterEngine.high_pass(filtered_signal, cutoff_freq * 1.05)
                    if logger:
                        logger.info(f"OK: Applied Notch filter at {cutoff_freq} Hz")
            
            # Compute FFT
            spectrum = FFTEngine.compute_fft(filtered_signal, window_type=window_type, zero_pad=zero_pad)
            if logger:
                logger.info(f"OK: FFT computed: {len(spectrum.freqs)} frequencies")
            
            # Detect peaks
            peaks = PeakDetector.detect_peaks(spectrum)
            if logger:
                logger.info(f"OK: Detected {len(peaks)} peaks")
            
            # Store results
            st.session_state.analysis_data = {
                "signal": signal_data,
                "filtered_signal": filtered_signal,
                "spectrum": spectrum,
                "peaks": peaks,
                "timestamp": datetime.now(),
            }
            
            # Track in session history
            if session_mgr:
                session_mgr.add_to_history("analysis", {
                    "signal_type": "generated" if 'imported_signal' not in st.session_state else "imported",
                    "fs": fs,
                    "num_peaks": len(peaks),
                })
                session_mgr.increment_analysis_count()
            
            duration_ms = (time.time() - start_time) * 1000
            if logger:
                logger.info(f"TIMER: Analysis completed in {duration_ms:.2f}ms")
            
            st.success("✅ Analysis Complete!")
            
        except Exception as e:
            if logger:
                logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            st.error(f"❌ Analysis Error: {str(e)}")
            st.info("💡 Try adjusting signal parameters or check the logs for details")

# ============================================================================
# MAIN DASHBOARD - INTERACTIVE PLOTS
# ============================================================================

if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    signal = data["signal"]
    filtered = data["filtered_signal"]
    spectrum = data["spectrum"]
    peaks = data["peaks"]
    
    st.markdown("### 📊 REAL-TIME ANALYSIS DASHBOARD")
    
    # Create all plots once for display and export
    fig_time, fig_freq, fig_phase, fig_psd = create_all_plots(signal, spectrum, peaks)
    
    # Store in session state for export
    st.session_state.figures = {
        'Time-Domain Signal': fig_time,
        'Frequency Spectrum': fig_freq,
        'Phase Spectrum': fig_phase,
        'Power Spectral Density': fig_psd,
    }
    
    # ========== METRICS ROW ==========
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Dominant Frequency",
            f"{peaks[0].frequency:.1f}" if peaks else "N/A",
            "Hz",
            "#00D4FF"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Peak Magnitude",
            f"{peaks[0].magnitude:.3f}" if peaks else "N/A",
            "",
            "#39FF14"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "SNR Level",
            f"{snr_db}",
            "dB",
            "#FF006E"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Detected Peaks",
            f"{len(peaks)}",
            "peaks",
            "#00D4FF"
        ), unsafe_allow_html=True)
    
    st.markdown("")
    
    # ========== PLOTS ROW 1 ==========
    st.markdown("<h3 style='color: #39FF14; border-bottom: 2px solid #39FF14; padding-bottom: 10px;'>📈 SPECTRAL ANALYSIS</h3>", unsafe_allow_html=True)
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⏱️ Time-Domain Signal**")
        st.markdown("<p style='color: #B0B9C6; font-size: 0.9em;'>Raw signal amplitude over time</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.markdown("**🎵 Frequency Spectrum (FFT)**")
        st.markdown("<p style='color: #B0B9C6; font-size: 0.9em;'>Magnitude spectrum with detected peaks</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    st.markdown("")
    
    # ========== PLOTS ROW 2 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔄 Phase Spectrum**")
        st.markdown("<p style='color: #B0B9C6; font-size: 0.9em;'>Phase angles across frequencies</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_phase, use_container_width=True)
    
    with col2:
        st.markdown("**⚡ Power Spectral Density**")
        st.markdown("<p style='color: #B0B9C6; font-size: 0.9em;'>Power distribution per frequency unit</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_psd, use_container_width=True)
    
    st.markdown("")
    
    # ========== PEAKS TABLE ==========
    st.markdown("<h3 style='color: #FF006E; border-bottom: 2px solid #FF006E; padding-bottom: 10px;'>🎯 DETECTED FREQUENCY PEAKS</h3>", unsafe_allow_html=True)
    
    if peaks:
        peaks_df = pd.DataFrame([
            {
                "🏆 Rank": i + 1,
                "📍 Frequency (Hz)": f"{p.frequency:.2f}",
                "📊 Magnitude": f"{p.magnitude:.6f}",
                "📈 Magnitude (dB)": f"{p.magnitude_db:.2f}",
                "📌 Prominence": f"{p.prominence:.6e}",
            }
            for i, p in enumerate(peaks[:20])
        ])
        
        st.markdown("<p style='color: #B0B9C6; font-size: 0.9em;'>Top 20 peaks by prominence</p>", unsafe_allow_html=True)
        st.dataframe(peaks_df, use_container_width=True, hide_index=True)
    else:
        st.info("🔍 No peaks detected in current signal configuration")
    
    st.markdown("")
    
    # ========== AI FEATURES SECTION ==========
    st.markdown("---")
    st.markdown("<h3 style='color: #00D4FF; border-bottom: 2px solid #00D4FF; padding-bottom: 10px;'>🤖 AI-ENHANCED FEATURES</h3>", unsafe_allow_html=True)
    
    ai_tab1, ai_tab2, ai_tab3 = st.tabs(["🗜️ Data Compression", "🚨 Anomaly Detection", "🧠 Signal Classification"])
    
    with ai_tab1:
        st.markdown("**Frequency Selection Compression**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            compression_ratio = st.slider(
                "Compression Level",
                0.1, 1.0, 0.7,
                step=0.05,
                help="Lower = more compression, higher quality = slower"
            )
        
        with col2:
            compress_button = st.button("🗜️ Compress", width='stretch')
        
        with col3:
            st.metric("Level", f"{compression_ratio*100:.0f}%")
        
        if compress_button:
            try:
                from src.fft_analyzer.ai import CompressionEngine
                
                with st.spinner("⏳ Compressing data..."):
                    compress_result = CompressionEngine.compress_spectrum(spectrum, compression_ratio)
                
                if compress_result:
                    # Create compressed spectrum plot
                    fig_compressed = go.Figure()
                    
                    # Original
                    fig_compressed.add_trace(go.Scatter(
                        x=spectrum.freqs,
                        y=spectrum.magnitude,
                        mode='lines',
                        name='Original',
                        line=dict(color='#00D4FF', width=2, dash='solid'),
                        opacity=0.7
                    ))
                    
                    # Compressed
                    fig_compressed.add_trace(go.Scatter(
                        x=compress_result['freqs'],
                        y=compress_result['magnitude'],
                        mode='lines',
                        name='Compressed',
                        line=dict(color='#39FF14', width=2, dash='dash'),
                    ))
                    
                    fig_compressed.update_layout(
                        title="📊 Original vs Compressed Spectrum",
                        height=400,
                        template="plotly_dark",
                        paper_bgcolor="#0A0E27",
                        plot_bgcolor="#1A1F3A",
                        font=dict(color="#FFFFFF"),
                        hovermode="x unified",
                    )
                    
                    st.plotly_chart(fig_compressed, use_container_width=True)
                    
                    # Metrics
                    metrics_cols = st.columns(4)
                    
                    with metrics_cols[0]:
                        st.metric(
                            "Compression",
                            f"{compress_result['compression_ratio']*100:.1f}%"
                        )
                    
                    with metrics_cols[1]:
                        st.metric(
                            "Energy Preserved",
                            f"{compress_result['energy_preserved']:.1f}%"
                        )
                    
                    with metrics_cols[2]:
                        st.metric(
                            "SNR",
                            f"{compress_result['snr_db']:.2f} dB"
                        )
                    
                    with metrics_cols[3]:
                        st.metric(
                            "MSE",
                            f"{compress_result['mse']:.2e}"
                        )
                    
                    # Details
                    with st.expander("📋 Compression Details"):
                        st.write(compress_result['info'])
                    
                    # Store for export
                    st.session_state.compressed_spectrum = compress_result
                    st.success("✅ Compression complete!")
                    
            except ImportError:
                st.error("❌ CompressionEngine not available")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with ai_tab2:
        st.markdown("**Isolation Forest Anomaly Detection**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            anomaly_threshold = st.slider(
                "Contamination Rate",
                0.01, 0.5, 0.1,
                step=0.01,
                help="Expected proportion of anomalies"
            )
        
        with col2:
            detect_button = st.button("🔍 Detect", width='stretch')
        
        with col3:
            st.metric("Threshold", f"{anomaly_threshold*100:.1f}%")
        
        if detect_button:
            try:
                from src.fft_analyzer.ai import AnomalyDetector
                
                with st.spinner("⏳ Detecting anomalies..."):
                    anomaly_result = AnomalyDetector.detect_spectrum_anomalies(
                        spectrum, contamination=anomaly_threshold
                    )
                
                if anomaly_result:
                    # Create anomaly plot
                    fig_anomaly = go.Figure()
                    
                    # Spectrum with anomaly coloring
                    colors = ['#FF006E' if is_anom else '#39FF14' 
                             for is_anom in anomaly_result['is_anomaly']]
                    
                    fig_anomaly.add_trace(go.Scatter(
                        x=spectrum.freqs,
                        y=spectrum.magnitude,
                        mode='markers+lines',
                        name='Magnitude',
                        marker=dict(color=colors, size=6),
                        line=dict(color='#00D4FF', width=1),
                    ))
                    
                    fig_anomaly.update_layout(
                        title="📊 Anomaly Detection Results",
                        height=400,
                        template="plotly_dark",
                        paper_bgcolor="#0A0E27",
                        plot_bgcolor="#1A1F3A",
                        font=dict(color="#FFFFFF"),
                        xaxis_title="Frequency (Hz)",
                        yaxis_title="Magnitude",
                        hovermode="x unified",
                    )
                    
                    st.plotly_chart(fig_anomaly, use_container_width=True)
                    
                    # Metrics
                    metrics_cols = st.columns(3)
                    
                    with metrics_cols[0]:
                        st.metric(
                            "Anomalies Found",
                            f"{anomaly_result['anomaly_count']}"
                        )
                    
                    with metrics_cols[1]:
                        st.metric(
                            "Anomaly %",
                            f"{anomaly_result['anomaly_count']/len(spectrum.magnitude)*100:.1f}%"
                        )
                    
                    with metrics_cols[2]:
                        st.metric(
                            "Severity",
                            f"{anomaly_result['severity']*100:.1f}%"
                        )
                    
                    # Top anomalies
                    if anomaly_result['top_anomalies']:
                        with st.expander("🔴 Top Anomalous Frequencies"):
                            top_anom_df = pd.DataFrame([
                                {
                                    'Frequency (Hz)': f"{a['freq']:.2f}",
                                    'Magnitude': f"{a['magnitude']:.6f}",
                                    'Anomaly Score': f"{a['score']:.3f}"
                                }
                                for a in anomaly_result['top_anomalies']
                            ])
                            st.dataframe(top_anom_df, use_container_width=True, hide_index=True)
                    
                    # Details
                    with st.expander("📋 Anomaly Detection Details"):
                        st.write(anomaly_result['info'])
                    
                    st.session_state.anomaly_result = anomaly_result
                    st.success("✅ Anomaly detection complete!")
                    
            except ImportError:
                st.error("❌ AnomalyDetector not available")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with ai_tab3:
        st.markdown("**Neural Network Signal Classifier**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("🧠 Classifies signals into: Normal, Transient, Periodic, Chaotic, Noisy")
        
        with col2:
            classify_button = st.button("🔍 Classify", width='stretch', key="classify_btn")
        
        if classify_button:
            try:
                from src.fft_analyzer.ai import SignalClassifier
                
                with st.spinner("⏳ Classifying signal..."):
                    classify_result = SignalClassifier.classify_signal(signal, spectrum)
                
                if classify_result:
                    # Display primary classification with confidence
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Color-coded confidence bar
                        confidence = classify_result['primary_confidence']
                        color = '#39FF14' if confidence > 0.7 else '#FF006E' if confidence < 0.5 else '#00D4FF'
                        st.markdown(f"<h3 style='color: {color};'>{classify_result['primary_class']}</h3>", unsafe_allow_html=True)
                        st.metric("Confidence", f"{confidence*100:.1f}%")
                    
                    with col2:
                        st.markdown(f"<h3 style='color: #00D4FF;'>Secondary</h3>", unsafe_allow_html=True)
                        st.metric("Class", classify_result['secondary_class'])
                        st.metric("Confidence", f"{classify_result['secondary_confidence']*100:.1f}%")
                    
                    with col3:
                        # Radar-like metrics display
                        st.markdown(f"<h3 style='color: #39FF14;'>Signal Profile</h3>", unsafe_allow_html=True)
                        st.metric("Periodicity", f"{classify_result['periodicity']*100:.1f}%")
                        st.metric("Transients", f"{classify_result['transient']*100:.1f}%")
                    
                    # Classification scores for all categories
                    st.markdown("**📊 Classification Scores**")
                    scores_df = pd.DataFrame([
                        {
                            'Signal Type': category,
                            'Confidence': f"{score*100:.1f}%",
                            'Score': score
                        }
                        for category, score in sorted(
                            classify_result['all_scores'].items(), 
                            key=lambda x: x[1], 
                            reverse=True
                        )
                    ])
                    
                    # Create bar chart for scores
                    fig_scores = go.Figure()
                    fig_scores.add_trace(go.Bar(
                        y=list(classify_result['all_scores'].keys()),
                        x=[v*100 for v in classify_result['all_scores'].values()],
                        orientation='h',
                        marker=dict(
                            color=['#39FF14' if v > 0.5 else '#FF006E' for v in classify_result['all_scores'].values()],
                            opacity=0.8
                        ),
                        text=[f"{v*100:.1f}%" for v in classify_result['all_scores'].values()],
                        textposition='auto'
                    ))
                    
                    fig_scores.update_layout(
                        title="📊 Classification Confidence Scores",
                        height=300,
                        template="plotly_dark",
                        paper_bgcolor="#0A0E27",
                        plot_bgcolor="#1A1F3A",
                        font=dict(color="#FFFFFF"),
                        xaxis_title="Confidence %",
                        showlegend=False,
                        margin=dict(l=150)
                    )
                    
                    st.plotly_chart(fig_scores, use_container_width=True)
                    
                    # Signal characteristics
                    char_cols = st.columns(4)
                    
                    with char_cols[0]:
                        st.metric("Noise Level", f"{classify_result['noise_level']*100:.1f}%")
                    
                    with char_cols[1]:
                        st.metric("Chaos Index", f"{classify_result['chaos']*100:.1f}%")
                    
                    with char_cols[2]:
                        st.metric("Periodicity", f"{classify_result['periodicity']*100:.1f}%")
                    
                    with char_cols[3]:
                        st.metric("Transient Activity", f"{classify_result['transient']*100:.1f}%")
                    
                    # Detailed info
                    with st.expander("📋 Classification Details"):
                        st.write(classify_result['info'])
                    
                    st.session_state.classification_result = classify_result
                    st.success("✅ Classification complete!")
                    
            except ImportError:
                st.error("❌ SignalClassifier not available")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("")
    
    # ========== ADVANCED ANALYSIS SECTION ==========
    st.markdown("---")
    st.markdown("<h3 style='color: #FF9500; border-bottom: 2px solid #FF9500; padding-bottom: 10px;'>⚙️ ADVANCED ANALYSIS</h3>", unsafe_allow_html=True)
    
    adv_tab1, adv_tab2 = st.tabs(["📊 Spectrogram (Time-Frequency)", "📈 Statistical Summary"])
    
    with adv_tab1:
        st.markdown("**Time-Frequency Analysis**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            window_size = st.slider(
                "FFT Window Size",
                64, 2048, 256,
                step=64,
                help="Larger = better frequency resolution, lower = better time resolution"
            )
        
        with col2:
            overlap = st.slider(
                "Window Overlap",
                0.25, 0.95, 0.75,
                step=0.05,
                help="Amount of overlap between windows"
            )
        
        with col3:
            spectrogram_button = st.button("🎬 Generate", width='stretch', key="spectrogram_btn")
        
        if spectrogram_button:
            try:
                from src.fft_analyzer.visualization import SpectrogramGenerator
                import plotly.graph_objects as go
                
                with st.spinner("⏳ Computing spectrogram..."):
                    spec_result = SpectrogramGenerator.generate_spectrogram(signal, window_size, overlap)
                
                if spec_result:
                    # Create spectrogram heatmap
                    fig_spec = go.Figure(data=go.Heatmap(
                        z=spec_result['magnitude_db'],
                        x=spec_result['times'],
                        y=spec_result['frequencies'],
                        colorscale='Viridis',
                        colorbar=dict(title="Power (dB)")
                    ))
                    
                    fig_spec.update_layout(
                        title="<b>Spectrogram (Time-Frequency Power)</b>",
                        xaxis_title="Time (s)",
                        yaxis_title="Frequency (Hz)",
                        height=600,
                        template="plotly_dark"
                    )
                    
                    st.plotly_chart(fig_spec, use_container_width=True)
                    st.success(spec_result['info'])
                    st.session_state.spectrogram_result = spec_result
                    
            except ImportError as e:
                st.error(f"❌ Spectrogram not available: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with adv_tab2:
        st.markdown("**Signal and Spectrum Statistics**")
        
        stats_button = st.button("📊 Analyze", width='stretch', key="stats_btn")
        
        if stats_button:
            try:
                from src.fft_analyzer.visualization import StatisticalAnalyzer
                
                with st.spinner("⏳ Computing statistics..."):
                    stats_result = StatisticalAnalyzer.analyze_signal_statistics(signal, spectrum)
                
                if stats_result:
                    # Create tabs for different stat categories
                    stats_col1, stats_col2 = st.columns(2)
                    
                    with stats_col1:
                        st.markdown("**⏱️ Time-Domain Statistics**")
                        time_stats = stats_result['time_domain']
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Mean", f"{time_stats['mean']:.6f}")
                            st.metric("RMS", f"{time_stats['rms']:.6f}")
                            st.metric("Peak", f"{time_stats['peak']:.6f}")
                        with col_b:
                            st.metric("Std Dev", f"{time_stats['std']:.6f}")
                            st.metric("Crest Factor", f"{time_stats['crest_factor']:.3f}")
                            st.metric("Peak-to-Peak", f"{time_stats['peak_to_peak']:.6f}")
                        
                        col_c, col_d = st.columns(2)
                        with col_c:
                            st.metric("Skewness", f"{time_stats['skewness']:.3f}")
                        with col_d:
                            st.metric("Kurtosis", f"{time_stats['kurtosis']:.3f}")
                    
                    with stats_col2:
                        st.markdown("**🎵 Frequency-Domain Statistics**")
                        freq_stats = stats_result['frequency_domain']
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Total Power", f"{freq_stats['total_power']:.2e}")
                            st.metric("Energy", f"{freq_stats['energy']:.6f}")
                            st.metric("PAPR", f"{freq_stats['papr']:.3f}")
                        with col_b:
                            st.metric("Variance", f"{freq_stats['variance']:.6f}")
                            st.metric("Dominant Freq", f"{freq_stats['dominant_frequency']:.1f} Hz")
                    
                    st.success("✅ Statistical analysis complete!")
                    st.session_state.stats_result = stats_result
                    
            except ImportError:
                st.error("❌ StatisticalAnalyzer not available")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("")
    
    # ========== EXPORT SECTION ==========
    st.markdown("---")
    st.markdown("<h3 style='color: #39FF14; border-bottom: 2px solid #39FF14; padding-bottom: 10px;'>⬇️ EXPORT ANALYSIS RESULTS</h3>", unsafe_allow_html=True)
    
    if export_button:
        st.markdown("<div style='padding: 20px; background-color: #1a3a3a; border-left: 4px solid #39FF14; border-radius: 6px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        st.info("📥 **Exporting analysis to Excel/CSV format...**")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====== EXCEL/CSV EXPORT ONLY ======
        try:
            print("\n✅ Exporting to Excel...")
            
            # Create spectrum DataFrame
            spectrum_df = pd.DataFrame({
                'Frequency (Hz)': spectrum.freqs,
                'Magnitude': spectrum.magnitude,
                'Phase (rad)': spectrum.phase,
                'PSD (V²/Hz)': spectrum.psd,
            })
            
            # Create peaks DataFrame
            peaks_data = []
            for i, peak in enumerate(peaks[:20]):
                peaks_data.append({
                    'Rank': i + 1,
                    'Frequency (Hz)': peak.frequency,
                    'Magnitude': peak.magnitude,
                    'Magnitude (dB)': peak.magnitude_db,
                    'Prominence': peak.prominence,
                })
            peaks_df = pd.DataFrame(peaks_data) if peaks_data else pd.DataFrame()
            
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                spectrum_df.to_excel(writer, sheet_name='Spectrum', index=False)
                if not peaks_df.empty:
                    peaks_df.to_excel(writer, sheet_name='Peaks', index=False)
            
            output.seek(0)
            excel_bytes = output.getvalue()
            
            st.download_button(
                label="📊 Download Excel File",
                data=excel_bytes,
                file_name=f"spectrum_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch'
            )
            print("✅ Excel export ready")
            st.success("✅ Excel file ready for download!")
            
        except Exception as e:
            st.error(f"❌ Excel export error: {str(e)}")
            print(f"Excel Error: {str(e)}")

    else:
        st.info("💾 Click the EXPORT button in the sidebar to download analysis results")

else:
    st.info("👈 **Configure parameters in the sidebar and click ANALYZE to start!**")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #B0B9C6; font-size: 12px; margin-top: 20px;">
    <p>🚀 AI-Enhanced Spectrum Analyzer v1.0 | Real-Time Signal Processing</p>
    <p>Built with Shlok using Streamlit, NumPy, SciPy, and Plotly</p>
</div>
""", unsafe_allow_html=True)
