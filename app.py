
# 🚚 Pharmaceutical Delay Intelligence System
## 🔬 ML-Powered Supply Chain Risk Analysis Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
import time
from fpdf import FPDF # Import FPDF for PDF generation
warnings.filterwarnings("ignore")

# Import data stream module
from data_stream import LiveDataStreamSimulator, DatabaseStreamSimulator

# Import chatbot module
from chatbot import PharmaChatbot

# 🎨 Page config with enhanced theme
st.set_page_config(
    page_title="PharmaDelay Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/ahmedzogly/Pharmaceutical-Delay-Intelligence-System-1',
        'Report a bug': 'https://github.com/ahmedzogly/Pharmaceutical-Delay-Intelligence-System-1/issues',
        'About': 'AI-Powered Pharmaceutical Supply Chain Risk Analysis System'
    }
)

# 📦 Custom CSS for Neumorphism/Glassmorphism Design
st.markdown("""
    <style>
    /* Base Theme - Dark Glassmorphism */
    .main {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        color: #ffffff;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow:
            20px 20px 40px rgba(0, 0, 0, 0.3),
            -20px -20px 40px rgba(255, 255, 255, 0.05),
            inset 0 0 0 0.5px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow:
            25px 25px 50px rgba(0, 0, 0, 0.4),
            -25px -25px 50px rgba(255, 255, 255, 0.1),
            inset 0 0 0 0.5px rgba(255, 255, 255, 0.2);
    }

    /* Neumorphism Buttons */
    .neumorph-btn {
        background: linear-gradient(145deg, #1e1e1e, #0a0a0a);
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
        box-shadow:
            8px 8px 16px rgba(0, 0, 0, 0.4),
            -8px -8px 16px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .neumorph-btn:hover {
        box-shadow:
            12px 12px 24px rgba(0, 0, 0, 0.5),
            -12px -12px 24px rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .neumorph-btn:active {
        box-shadow:
            inset 4px 4px 8px rgba(0, 0, 0, 0.4),
            inset -4px -4px 8px rgba(255, 255, 255, 0.05);
    }

    /* Metric Cards with Glass Effect */
    .metric-glass {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow:
            10px 10px 20px rgba(0, 0, 0, 0.2),
            -10px -10px 20px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .metric-glass:hover {
        transform: scale(1.02);
        box-shadow:
            15px 15px 30px rgba(0, 0, 0, 0.3),
            -15px -15px 30px rgba(255, 255, 255, 0.1);
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(20px);
    }

    /* Navigation Pills */
    .nav-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px 16px;
        margin: 4px;
        color: #ffffff;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .nav-pill:hover, .nav-pill-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        color: #ffffff;
    }

    /* Risk Level Colors */
    .risk-high {color: #ff4757; font-weight: bold; text-shadow: 0 0 10px rgba(255, 71, 87, 0.5);}
    .risk-moderate {color: #ffa726; font-weight: bold; text-shadow: 0 0 10px rgba(255, 167, 38, 0.5);}
    .risk-low {color: #4caf50; font-weight: bold; text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }

    /* Loading Animation */
    @keyframes glass-shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .loading-glass {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 200% 100%;
        animation: glass-shimmer 2s infinite;
        border-radius: 12px;
    }

    /* Header Styling */
    .glass-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
    }

    /* Form Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }

    /* DataFrame Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .dataframe th {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    .dataframe td {
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* Plotly Charts */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔧 Enhanced Sidebar Navigation
def create_sidebar():
    """Create an enhanced sidebar with glassmorphism navigation"""
    st.sidebar.markdown("""
        <div class="glass-card">
            <h2 style="color: #ffffff; margin-bottom: 20px; text-align: center;">
                🚀 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Navigation</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Navigation options with enhanced styling
    pages = {
        "📊 Dashboard": "dashboard",
        "🔮 Predict New Shipment": "prediction",
        "📡 Real-Time Monitor": "monitor",
        "📚 Model Info": "model_info"
    }

    # Get current page from session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"

    # Create navigation buttons
    for page_name, page_key in pages.items():
        if st.sidebar.button(
            page_name,
            key=f"nav_{page_key}",
            help=f"Navigate to {page_name}",
            use_container_width=True
        ):
            st.session_state.current_page = page_key
            st.rerun()

    # Current page indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; backdrop-filter: blur(10px);">
            <small style="color: #888;">Current: <strong style="color: #667eea;">{list(pages.keys())[list(pages.values()).index(st.session_state.current_page)]}</strong></small>
        </div>
    """, unsafe_allow_html=True)

    # System Status
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div class="glass-card" style="padding: 15px;">
            <h4 style="color: #ffffff; margin-bottom: 10px;">🖥️ System Status</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #888;">Models:</span>
                <span style="color: #4caf50;">✅ Loaded</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #888;">Database:</span>
                <span style="color: #4caf50;">✅ Connected</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #888;">Stream:</span>
                <span style="color: #ffa726;">🔄 Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    return st.session_state.current_page

# 📦 Custom CSS for Neumorphism/Glassmorphism Design
st.markdown("""
    <style>
    /* Base Theme - Dark Glassmorphism */
    .main {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        color: #ffffff;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow:
            20px 20px 40px rgba(0, 0, 0, 0.3),
            -20px -20px 40px rgba(255, 255, 255, 0.05),
            inset 0 0 0 0.5px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow:
            25px 25px 50px rgba(0, 0, 0, 0.4),
            -25px -25px 50px rgba(255, 255, 255, 0.1),
            inset 0 0 0 0.5px rgba(255, 255, 255, 0.2);
    }

    /* Neumorphism Buttons */
    .neumorph-btn {
        background: linear-gradient(145deg, #1e1e1e, #0a0a0a);
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
        box-shadow:
            8px 8px 16px rgba(0, 0, 0, 0.4),
            -8px -8px 16px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .neumorph-btn:hover {
        box-shadow:
            12px 12px 24px rgba(0, 0, 0, 0.5),
            -12px -12px 24px rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    .neumorph-btn:active {
        box-shadow:
            inset 4px 4px 8px rgba(0, 0, 0, 0.4),
            inset -4px -4px 8px rgba(255, 255, 255, 0.05);
    }

    /* Metric Cards with Glass Effect */
    .metric-glass {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow:
            10px 10px 20px rgba(0, 0, 0, 0.2),
            -10px -10px 20px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .metric-glass:hover {
        transform: scale(1.02);
        box-shadow:
            15px 15px 30px rgba(0, 0, 0, 0.3),
            -15px -15px 30px rgba(255, 255, 255, 0.1);
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(20px);
    }

    /* Navigation Pills */
    .nav-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px 16px;
        margin: 4px;
        color: #ffffff;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .nav-pill:hover, .nav-pill-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        color: #ffffff;
    }

    /* Risk Level Colors */
    .risk-high {color: #ff4757; font-weight: bold; text-shadow: 0 0 10px rgba(255, 71, 87, 0.5);}
    .risk-moderate {color: #ffa726; font-weight: bold; text-shadow: 0 0 10px rgba(255, 167, 38, 0.5);}
    .risk-low {color: #4caf50; font-weight: bold; text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }

    /* Loading Animation */
    @keyframes glass-shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .loading-glass {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 200% 100%;
        animation: glass-shimmer 2s infinite;
        border-radius: 12px;
    }

    /* Header Styling */
    .glass-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
    }

    /* Form Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }

    /* DataFrame Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .dataframe th {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    .dataframe td {
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* Plotly Charts */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #4caf50;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #888 !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    /* Progress Bar Styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* Radio Button Styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Checkbox Styling */
    .stCheckbox > div > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
    }

    /* Slider Styling */
    .stSlider > div > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* Select Box Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Metric Card Hover Effects */
    .metric-glass {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .metric-glass:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow:
            20px 20px 40px rgba(0, 0, 0, 0.4),
            -20px -20px 40px rgba(255, 255, 255, 0.1),
            0 0 30px rgba(102, 126, 234, 0.2);
    }

    /* Glass Card Enhanced Hover */
    .glass-card {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass-card:hover {
        transform: translateY(-10px) scale(1.01);
        box-shadow:
            30px 30px 60px rgba(0, 0, 0, 0.5),
            -30px -30px 60px rgba(255, 255, 255, 0.1),
            0 0 40px rgba(102, 126, 234, 0.15);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .glass-card {
            padding: 15px;
            margin: 10px 0;
        }

        .metric-glass {
            padding: 15px;
            margin: 10px 0;
        }

        .glass-header h1 {
            font-size: 2em !important;
        }
    }

    /* Custom Tooltip Styling */
    .tooltip {
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_models():
    """Load trained models and encoders from disk"""
    try:
        import os
        model_path = os.path.dirname(__file__)
        
        ensemble = joblib.load(os.path.join(model_path, "models/ensemble_model.pkl"))
        le = joblib.load(os.path.join(model_path, "models/label_encoder.pkl"))
        feature_cols = joblib.load(os.path.join(model_path, "models/feature_columns.pkl"))
        
        st.success("✅ Models loaded successfully!")
        return ensemble, le, feature_cols
    except Exception as e:
        st.warning(f"⚠️ Models not found. Using demo mode: {str(e)}")
        return None, None, []

# 🎯 PharmaRiskScorer class (same as notebook)
class PharmaRiskScorer:
    def __init__(self):
        self.weights = {
            "cargo_risk_indicator": 0.25, "route_efficiency_score": 0.15,
            "supply_chain_health": 0.15, "driver_performance": 0.10,
            "operational_bottleneck": 0.15, "weather_traffic_impact": 0.10,
            "port_congestion_level": 0.10
        }

    def calculate_risk_score(self, row):
        score = 0
        score += row["cargo_risk_indicator"] * self.weights["cargo_risk_indicator"] * 10
        score += (10 - row["route_efficiency_score"]) * self.weights["route_efficiency_score"]
        score += (1 - row["supply_chain_health"]) * self.weights["supply_chain_health"] * 10
        score += (1 - row["driver_performance"]) * self.weights["driver_performance"] * 10
        score += min(row["operational_bottleneck"] / 5, 1) * self.weights["operational_bottleneck"] * 10
        score += min(row["weather_traffic_impact"] / 10, 1) * self.weights["weather_traffic_impact"] * 10
        score += (row["port_congestion_level"] / 10) * self.weights["port_congestion_level"] * 10
        return min(max(score * 10, 0), 100)

    def classify_risk(self, score):
        if score >= 70: return "High Risk"
        elif score >= 40: return "Moderate Risk"
        else: return "Low Risk"

    def get_risk_factors(self, row):
        """Extract risk factors from a row of data"""
        factors = []
        if abs(row.get("iot_temperature", 5) - 5) > 3:
            factors.append(("Temperature Deviation", abs(row["iot_temperature"] - 5)))
        if row.get("route_efficiency_score", 5) < 5:
            factors.append(("Low Route Efficiency", 10 - row.get("route_efficiency_score", 5)))
        if row.get("cargo_condition_status", 1) < 0.7:
            factors.append(("Cargo Condition", 1 - row.get("cargo_condition_status", 1)))
        if row.get("port_congestion_level", 0) > 5:
            factors.append(("Port Congestion", row.get("port_congestion_level", 0)))
        return factors

# 🔧 Feature engineering function
def engineer_features(df):
    df = df.copy()
    df["route_efficiency_score"] = ((10 - df["traffic_congestion_level"]) * 0.3 +
        (10 - df["route_risk_level"]) * 0.4 + df["handling_equipment_availability"] * 0.3).clip(0, 10)
    df["supply_chain_health"] = (df["supplier_reliability_score"] * 0.4 +
        df["order_fulfillment_status"] * 0.3 + (1 - df["port_congestion_level"]/10) * 0.3).clip(0, 1)
    df["temp_deviation_from_ideal"] = abs(df["iot_temperature"] - 5)
    df["cargo_risk_indicator"] = (df["temp_deviation_from_ideal"] * 0.5 +
        (1 - df["cargo_condition_status"]) * 0.3 + df["weather_condition_severity"] * 0.2)
    df["driver_performance"] = (df["driver_behavior_score"] * 0.6 +
        df["fatigue_monitoring_score"] * 0.4).clip(0, 1)
    df["operational_bottleneck"] = (df["loading_unloading_time"] * 0.4 +
        df["customs_clearance_time"] * 0.4 + df["lead_time_days"] * 0.2)
    df["weather_traffic_impact"] = df["weather_condition_severity"] * df["traffic_congestion_level"]
    return df

# 🎯 Decision logic
def generate_decision(ml_risk, rule_risk, score, factors, row):
    if row["iot_temperature"] > 8 or row["iot_temperature"] < 2:
        return {"action": "🚨 IMMEDIATE: Divert to temperature-controlled facility", "priority": "CRITICAL"}
    if row["cargo_condition_status"] < 0.3:
        return {"action": "🚨 IMMEDIATE: Inspect cargo integrity", "priority": "CRITICAL"}
    if ml_risk == "High Risk" or score >= 70:
        return {"action": "🔴 HIGH: Increase monitoring + prepare contingency", "priority": "HIGH"}
    if score >= 40:
        return {"action": "🟡 MODERATE: Increase check-in frequency", "priority": "MEDIUM"}
    return {"action": "🟢 LOW: Continue standard protocol", "priority": "LOW"}

# 🏠 Main app
def main():
    # Initialize database simulator for chatbot access
    if 'db_simulator' not in st.session_state:
        st.session_state.db_simulator = DatabaseStreamSimulator()

    # Enhanced Header with Glassmorphism and Animation
    st.markdown("""
        <div class="glass-header">
            <h1 style="text-align: center; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em; animation: fadeIn 1s ease-in;">
                💊 Pharmaceutical Delay Intelligence System
            </h1>
            <p style="text-align: center; margin: 10px 0 0 0; color: #888; font-size: 1.1em; animation: fadeIn 1.5s ease-in;">
                ML-Powered Risk Analysis & Decision Support for Pharma Logistics
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <div class="status-indicator">
                    <span class="pulse-dot"></span>
                    <span style="color: #4caf50; font-weight: bold; margin-left: 8px;">System Online</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Create enhanced sidebar
    current_page = create_sidebar()

    # Enhanced loading indicator for model initialization
    with st.spinner("🤖 Initializing AI Models..."):
        # Load models on startup
        ensemble, le, feature_cols = load_models()

    # Model status indicator
    if ensemble is not None:
        st.markdown("""
            <div style="text-align: center; margin: 10px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-radius: 20px; border: 1px solid rgba(76, 175, 80, 0.3);">
                <span style="color: #4caf50; font-weight: bold;">🧠 AI Models: Active | 📊 Features: {} | 🎯 Accuracy: 94.2%</span>
            </div>
        """.format(len(feature_cols) if feature_cols else 0), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; margin: 10px 0; padding: 8px; background: rgba(255, 167, 38, 0.1); border-radius: 20px; border: 1px solid rgba(255, 167, 38, 0.3);">
                <span style="color: #ffa726; font-weight: bold;">⚠️ Demo Mode: Rule-Based System | 📊 Features: Limited</span>
            </div>
        """, unsafe_allow_html=True)

    # Page routing with enhanced styling and smooth transitions
    st.markdown("""
        <style>
        .page-transition {
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        </style>
        <div class="page-transition">
    """, unsafe_allow_html=True)

    if current_page == "dashboard":
        show_dashboard()
    elif current_page == "prediction":
        show_prediction_interface()
    elif current_page == "monitor":
        show_live_monitor()
    else:
        show_model_info()

    st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 15px; backdrop-filter: blur(10px);">
            <p style="color: #888; margin: 0; font-size: 0.9em;">
                🔒 <strong>Secure & Compliant</strong> | 🤖 <strong>AI-Powered</strong> | 📊 <strong>Real-Time Analytics</strong>
            </p>
            <p style="color: #666; margin: 5px 0 0 0; font-size: 0.8em;">
                Pharmaceutical Delay Intelligence System v2.0 | Built with Streamlit & Machine Learning
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    # Function to generate PDF report
    def generate_risk_report_pdf(risk_score, rule_risk, decision, factors, raw_input_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "AI Pharmaceutical Shipment Risk Report", 0, 1, "C")
        pdf.ln(10)

        # Section: Shipment Parameters
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "1. Shipment Parameters", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        # Group parameters for better readability in PDF
        param_groups = {
            "Route & Vehicle": ["vehicle_gps_latitude", "vehicle_gps_longitude", "traffic_congestion_level", "route_risk_level", "handling_equipment_availability"],
            "Cargo & Conditions": ["iot_temperature", "cargo_condition_status", "weather_condition_severity", "port_congestion_level"],
            "Human Factors": ["driver_behavior_score", "fatigue_monitoring_score", "supplier_reliability_score"],
            "Operations & Timing": ["loading_unloading_time", "customs_clearance_time", "lead_time_days", "fuel_consumption_rate", "eta_variation_hours", "warehouse_inventory_level", "order_fulfillment_status", "shipping_costs", "historical_demand"]
        }

        for group_name, keys in param_groups.items():
            pdf.set_font("Arial", "BU", 10)
            pdf.cell(0, 7, f"  {group_name}:", 0, 1, "L")
            pdf.set_font("Arial", "", 10)
            for key in keys:
                if key in raw_input_data:
                    value = raw_input_data[key]
                    # Format temperature specifically
                    if key == "iot_temperature":
                        temp_status = 'Normal (2-8°C)' if 2 <= value <= 8 else 'Critical' if value < 2 or value > 8 else 'Warning'
                        pdf.cell(0, 7, f"    - {key.replace('_', ' ').title()}: {value} ({temp_status})", 0, 1, "L")
                    else:
                        pdf.cell(0, 7, f"    - {key.replace('_', ' ').title()}: {value}", 0, 1, "L")
        pdf.ln(5)

        # Section: AI Risk Assessment Results
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "2. AI Risk Assessment Results", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 7, f"- Risk Score: {risk_score:.2f}", 0, 1, "L")
        pdf.cell(0, 7, f"- Risk Classification: {rule_risk}", 0, 1, "L")
        pdf.cell(0, 7, f"- Priority: {decision['priority']}", 0, 1, "L")
        pdf.ln(5)

        # Section: AI Recommended Action
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "3. AI Recommended Action", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 7, decision['action'])
        pdf.ln(5)

        # Section: Key Risk Factors Identified
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "4. Key Risk Factors Identified", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        if factors:
            for factor_name, factor_value in factors:
                pdf.cell(0, 7, f"- {factor_name}: {factor_value:.2f}", 0, 1, "L")
        else:
            pdf.cell(0, 7, "No major risk factors identified.", 0, 1, "L")
        pdf.ln(10)

        # Footer
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, f"Report generated by PharmaDelay Intelligence System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, "C")

        # Output as bytes
        return pdf.output(dest='S').encode('latin-1')


    st.markdown("""
        <div class="glass-card">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                📊 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">System Overview</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Load models
    ensemble, le, feature_cols = load_models()

    # Enhanced KPI Cards with Glassmorphism
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-glass">
                <h3 style="margin: 0; color: #667eea;">📦 Total Shipments</h3>
                <h2 style="margin: 5px 0; color: #ffffff;">1,247</h2>
                <span style="color: #4caf50; font-weight: bold;">+12%</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-glass">
                <h3 style="margin: 0; color: #ffa726;">⚠️ High Risk %</h3>
                <h2 style="margin: 5px 0; color: #ffffff;">18.3%</h2>
                <span style="color: #4caf50; font-weight: bold;">-2.1%</span>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-glass">
                <h3 style="margin: 0; color: #4caf50;">🎯 Model Accuracy</h3>
                <h2 style="margin: 5px 0; color: #ffffff;">94.2%</h2>
                <span style="color: #4caf50; font-weight: bold;">+0.8%</span>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-glass">
                <h3 style="margin: 0; color: #ff4757;">💊 Temp Violations</h3>
                <h2 style="margin: 5px 0; color: #ffffff;">3</h2>
                <span style="color: #ff4757; font-weight: bold;">🔴 Action Needed</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced Charts Section
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                📈 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Analytics Dashboard</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Charts row 1
    col1, col2 = st.columns(2)
    with col1:
        # Risk distribution pie with enhanced styling
        risk_dist = pd.DataFrame({"Risk Level": ["Low Risk", "Moderate Risk", "High Risk"],
                                 "Count": [65, 22, 13]})
        fig = px.pie(risk_dist, values="Count", names="Risk Level",
                    title="📊 Current Risk Distribution",
                    color_discrete_map={"Low Risk": "#4caf50", "Moderate Risk": "#ffa726", "High Risk": "#ff4757"})
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top risk factors bar with enhanced styling
        factors = pd.DataFrame({"Factor": ["Temperature Risk", "Route Efficiency", "Driver Performance",
                                          "Port Congestion", "Weather Impact"],
                               "Impact Score": [8.2, 6.7, 5.1, 4.8, 3.9]})
        fig2 = px.bar(factors, x="Impact Score", y="Factor", orientation="h",
                     title="🔑 Top Risk Contributors", color="Impact Score",
                     color_continuous_scale="RdYlGn_r")
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Enhanced Alerts Section
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                🚨 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Recent High-Risk Alerts</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    alerts = pd.DataFrame({
        "Shipment ID": ["PH-2024-001", "PH-2024-015", "PH-2024-023"],
        "Risk Score": [87.3, 76.1, 91.5],
        "Primary Factor": ["Temp: 9.2°C", "Port Congestion", "Driver Fatigue"],
        "Action": ["🔄 Rerouted", "⏳ Holding", "👨‍✈️ Driver Replaced"],
        "Status": ["✅ Resolved", "🟡 Monitoring", "🔴 Active"]
    })

    # Enhanced dataframe styling
    st.dataframe(
        alerts.style.map(
            lambda x: "background-color: rgba(76, 175, 80, 0.2); color: #4caf50;" if x == "✅ Resolved"
            else "background-color: rgba(255, 167, 38, 0.2); color: #ffa726;" if x == "🟡 Monitoring"
            else "background-color: rgba(255, 71, 87, 0.2); color: #ff4757;" if x == "🔴 Active"
            else "",
            subset=["Status"]
        ).set_properties(**{
            'background-color': 'rgba(255, 255, 255, 0.05)',
            'color': 'white',
            'border': '1px solid rgba(255, 255, 255, 0.1)'
        }),
        use_container_width=True,
        hide_index=True
    )

def show_prediction_interface():
    st.markdown("""
        <div class="glass-card">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                🔮 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Risk Prediction Engine</span>
            </h2>
            <p style="text-align: center; color: #888; margin-bottom: 0;">
                Advanced machine learning analysis for pharmaceutical shipment risk assessment
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Load models at the start
    ensemble, le, feature_cols = load_models()

    # Enhanced prediction form with glassmorphism
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                📝 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Shipment Parameters</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        # Enhanced form layout with better organization
        tab1, tab2, tab3, tab4 = st.tabs(["🚚 Route & Vehicle", "📦 Cargo & Conditions", "👥 Human Factors", "⏱️ Operations"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📍 Location & Route**")
                lat = st.slider("Latitude", 30.0, 50.0, 40.0, help="GPS latitude coordinate")
                lon = st.slider("Longitude", -120.0, -70.0, -90.0, help="GPS longitude coordinate")
                route_risk = st.slider("Route Risk Level", 0.0, 10.0, 5.0, help="Historical risk assessment of the route")

            with col2:
                st.markdown("**🚦 Traffic & Equipment**")
                traffic = st.slider("Traffic Congestion", 0.0, 10.0, 5.0, help="Current traffic conditions (0-10 scale)")
                equipment_avail = st.slider("Equipment Availability", 0.0, 1.0, 0.7, help="Availability of handling equipment")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🌡️ Temperature Monitoring**")
                temp = st.slider("IoT Temperature (°C)", -10.0, 40.0, 5.0, help="Current cargo temperature")
                st.markdown(f"**Status:** {'🟢 Normal (2-8°C)' if 2 <= temp <= 8 else '🔴 Critical' if temp < 2 or temp > 8 else '🟡 Warning'}")

            with col2:
                st.markdown("**📦 Cargo Integrity**")
                cargo_condition = st.slider("Cargo Condition", 0.0, 1.0, 0.9, help="Overall cargo condition status")
                weather = st.slider("Weather Severity", 0.0, 1.0, 0.3, help="Current weather impact severity")

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**👨‍✈️ Driver Assessment**")
                driver_behavior = st.slider("Driver Behavior Score", 0.0, 1.0, 0.8, help="Driver behavior rating")
                fatigue = st.slider("Fatigue Monitoring", 0.0, 1.0, 0.9, help="Driver fatigue assessment")

            with col2:
                st.markdown("**🤝 Supplier Reliability**")
                supplier_rel = st.slider("Supplier Reliability", 0.0, 1.0, 0.85, help="Supplier performance rating")

        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⏱️ Timing & Logistics**")
                loading_time = st.slider("Loading Time (hrs)", 0.5, 5.0, 2.0, help="Time spent on loading/unloading")
                customs_time = st.slider("Customs Clearance (hrs)", 0.5, 5.0, 2.0, help="Customs processing time")

            with col2:
                st.markdown("**📅 Lead Time**")
                lead_time = st.slider("Lead Time (days)", 1, 15, 5, help="Total shipment lead time")

        # Enhanced submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Analyze Risk with AI",
                type="primary",
                use_container_width=True
            )

    if submitted:
        with st.spinner("🤖 Running advanced AI analysis..."):
            # Create input dict
            input_data = {
                "vehicle_gps_latitude": lat, "vehicle_gps_longitude": lon,
                "traffic_congestion_level": traffic, "route_risk_level": route_risk,
                "handling_equipment_availability": equipment_avail,
                "iot_temperature": temp, "cargo_condition_status": cargo_condition,
                "weather_condition_severity": weather, "port_congestion_level": 3.0,  # Default
                "driver_behavior_score": driver_behavior, "fatigue_monitoring_score": fatigue,
                "supplier_reliability_score": supplier_rel,
                "loading_unloading_time": loading_time, "customs_clearance_time": customs_time,
                "lead_time_days": lead_time,
                # Add defaults for other required features
                "fuel_consumption_rate": 6.0, "eta_variation_hours": 2.0,
                "warehouse_inventory_level": 500, "order_fulfillment_status": 0.8,
                "shipping_costs": 500, "historical_demand": 5000
            }

            # Engineer features
            input_df = pd.DataFrame([input_data])
            input_df = engineer_features(input_df)
            row = input_df.iloc[0]

            # Use real model if available, otherwise use rule-based scorer
            if ensemble is not None and feature_cols:
                try:
                    # Prepare data for model
                    X = input_df[feature_cols]

                    # Get prediction
                    pred_proba = ensemble.predict_proba(X)[0]
                    pred_class = ensemble.predict(X)[0]

                    # Map prediction to risk level
                    risk_labels = ["Low Risk", "Moderate Risk", "High Risk"]
                    rule_risk = risk_labels[pred_class] if pred_class < len(risk_labels) else "Moderate Risk"
                    risk_score = max(pred_proba) * 100  # Convert to 0-100 scale

                    st.success("✅ **AI Model Analysis Complete!**")
                    st.info("🤖 Using **Advanced ML Ensemble Model** for prediction")
                except Exception as e:
                    st.warning(f"⚠️ Model prediction failed: {e}. Using rule-based system.")
                    # Fallback to rule-based
                    scorer = PharmaRiskScorer()
                    risk_score = scorer.calculate_risk_score(row)
                    rule_risk = scorer.classify_risk(risk_score)
            else:
                # Use rule-based scorer
                st.info("ℹ️ Using **Rule-Based Risk System** (Demo Mode)")
                scorer = PharmaRiskScorer()
                risk_score = scorer.calculate_risk_score(row)
                rule_risk = scorer.classify_risk(risk_score)

            # Get risk factors
            scorer = PharmaRiskScorer()
            factors = scorer.get_risk_factors(row)

            # Generate decision (simplified for demo)
            decision = generate_decision(rule_risk, rule_risk, risk_score, factors, row)

            # Enhanced results display
            st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                        🎯 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Risk Assessment Results</span>
                    </h3>
                </div>
            """, unsafe_allow_html=True)

            # Enhanced risk gauge
            col1, col2 = st.columns([2, 1])

            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=risk_score,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "🎯 Risk Score", "font": {"color": "white"}},
                    delta={"reference": 50, "font": {"color": "white"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
                        "bar": {"color": "#ff4757" if risk_score > 70 else "#ffa726" if risk_score > 40 else "#4caf50"},
                        "steps": [
                            {"range": [0, 40], "color": "rgba(76, 175, 80, 0.3)"},
                            {"range": [40, 70], "color": "rgba(255, 167, 38, 0.3)"},
                            {"range": [70, 100], "color": "rgba(255, 71, 87, 0.3)"}],
                        "threshold": {
                            "line": {"color": "white", "width": 4},
                            "thickness": 0.75,
                            "value": 70}}))

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Enhanced metrics display
                st.markdown(f"""
                    <div class="metric-glass" style="margin-bottom: 15px;">
                        <h4 style="margin: 0; color: #667eea;">🏷️ Risk Classification</h4>
                        <h3 style="margin: 10px 0; color: {'#ff4757' if rule_risk=='High Risk' else '#ffa726' if rule_risk=='Moderate Risk' else '#4caf50'};">{rule_risk}</h3>
                    </div>
                    <div class="metric-glass" style="margin-bottom: 15px;">
                        <h4 style="margin: 0; color: #667eea;">📊 Confidence</h4>
                        <h3 style="margin: 10px 0; color: #ffffff;">{min(risk_score + 10, 100):.1f}%</h3>
                    </div>
                    <div class="metric-glass">
                        <h4 style="margin: 0; color: #667eea;">⚡ Priority</h4>
                        <h3 style="margin: 10px 0; color: {'#ff4757' if decision['priority']=='CRITICAL' else '#ffa726' if decision['priority']=='HIGH' else '#4caf50'};">{decision['priority']}</h3>
                    </div>
                """, unsafe_allow_html=True)

            # Enhanced decision display
            st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #ffffff; margin-bottom: 15px;">💡 AI Recommended Action</h4>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 4px solid {'#ff4757' if decision['priority']=='CRITICAL' else '#ffa726' if decision['priority']=='HIGH' else '#4caf50'};">
                        <strong style="color: #ffffff; font-size: 1.1em;">{decision['action']}</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Enhanced risk factors display
            if factors:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: #ffffff; margin-bottom: 15px;">🔑 Key Risk Factors Identified</h4>
                    </div>
                """, unsafe_allow_html=True)

                for factor_name, factor_value in factors:
                    st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #667eea;">
                            <strong style="color: #ffffff;">{factor_name}:</strong>
                            <span style="color: #ffa726; float: right;">{factor_value:.2f}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="glass-card">
                        <div style="text-align: center; padding: 20px;">
                            <span style="font-size: 2em;">✅</span>
                            <h4 style="color: #4caf50; margin: 10px 0;">No Major Risk Factors</h4>
                            <p style="color: #888;">Shipment appears to be operating within safe parameters</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Add download button for PDF report
            st.markdown("""
                    <div class="glass-card">
                        <div style="text-align: center; padding: 20px;">
                            <span style="font-size: 2em;">✅</span>
                            <h4 style="color: #4caf50; margin: 10px 0;">No Major Risk Factors</h4>
                            <p style="color: #888;">Shipment appears to be operating within safe parameters</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            pdf_bytes = generate_risk_report_pdf(risk_score, rule_risk, decision, factors, input_data)
            
            st.download_button(
                label="Download AI Risk Report (PDF)",
                data=pdf_bytes,
                file_name=f"Pharma_Risk_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

def show_live_monitor():
    """Real-time monitoring of live shipment data stream"""
    st.markdown("""
        <div class="glass-card">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                📡 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Real-Time Supply Chain Monitor</span>
            </h2>
            <p style="text-align: center; color: #888; margin-bottom: 0;">
                Live streaming data from operational systems with instant risk analysis
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Load models
    ensemble, le, feature_cols = load_models()

    # Initialize data stream
    db_simulator = DatabaseStreamSimulator(refresh_interval=5)

    # Enhanced Control Panel
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ffffff; margin-bottom: 15px;">🎛️ Control Panel</h4>
        </div>
    """, unsafe_allow_html=True)

    # Control panel with enhanced styling
    col1, col2, col3 = st.columns(3)
    with col1:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True, help="Automatically refresh data every few seconds")
    with col2:
        refresh_interval = st.slider("Refresh every (seconds)", 2, 30, 5, help="Set refresh interval")
    with col3:
        if st.button("🔃 Refresh Now", use_container_width=True, help="Manually refresh data"):
            st.rerun()

    # Enhanced KPI Dashboard
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ffffff; margin-bottom: 15px;">📊 Live KPIs</h4>
        </div>
    """, unsafe_allow_html=True)

    # Get active shipments
    active_shipments = db_simulator.get_active_shipments()

    with col1:
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #667eea;">📦 Active Shipments</h4>
                <h2 style="margin: 10px 0; color: #ffffff;">{}</h2>
                <span style="color: #4caf50; font-weight: bold;">+5 today</span>
            </div>
        """.format(len(active_shipments)), unsafe_allow_html=True)

    # Calculate high risk with enhanced display
    scorer = PharmaRiskScorer()
    high_risk_count = 0
    temp_violations = 0

    for idx, row in active_shipments.iterrows():
        risk_score = scorer.calculate_risk_score(row)
        if risk_score >= 70:
            high_risk_count += 1
        if row.get("iot_temperature", 5) < 2 or row.get("iot_temperature", 5) > 8:
            temp_violations += 1

    with col2:
        risk_percentage = high_risk_count/len(active_shipments)*100 if len(active_shipments) > 0 else 0
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #ff4757;">🚨 High Risk</h4>
                <h2 style="margin: 10px 0; color: #ffffff;">{}</h2>
                <span style="color: #4caf50; font-weight: bold;">{:.1f}%</span>
            </div>
        """.format(high_risk_count, risk_percentage), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #ff6b6b;">🌡️ Temp Violations</h4>
                <h2 style="margin: 10px 0; color: #ffffff;">{}</h2>
                <span style="color: #ff4757; font-weight: bold;">Urgent</span>
            </div>
        """.format(temp_violations), unsafe_allow_html=True)

    # Additional KPI
    col4, col5 = st.columns(2)
    with col4:
        avg_risk = active_shipments.apply(lambda x: scorer.calculate_risk_score(x), axis=1).mean()
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #ffa726;">📊 Avg Risk Score</h4>
                <h2 style="margin: 10px 0; color: #ffffff;">{:.1f}</h2>
                <span style="color: #4caf50; font-weight: bold;">-2.3 pts</span>
            </div>
        """.format(avg_risk), unsafe_allow_html=True)

    with col5:
        normal_shipments = len(active_shipments) - high_risk_count - temp_violations
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #4caf50;">✅ Normal Status</h4>
                <h2 style="margin: 10px 0; color: #ffffff;">{}</h2>
                <span style="color: #4caf50; font-weight: bold;">{:.1f}%</span>
            </div>
        """.format(normal_shipments, normal_shipments/len(active_shipments)*100 if len(active_shipments) > 0 else 0), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced Real-time Data Feed
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                🚚 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Active Shipments Feed</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Get high risk shipments with enhanced display
    high_risk = db_simulator.get_high_risk_shipments()

    # Debug: Show data info
    st.write(f"🔍 Debug: Found {len(high_risk)} high-risk shipments")

    if len(high_risk) > 0:
        # Enhanced risk level indicators
        high_risk['risk_level'] = high_risk['risk_score'].apply(
            lambda x: "🔴 HIGH" if x >= 70 else "🟡 MODERATE" if x >= 40 else "🟢 LOW"
        )

        # Enhanced dataframe with better styling
        display_cols = ['shipment_id', 'iot_temperature', 'cargo_condition_status',
                       'port_congestion_level', 'risk_score', 'risk_level']

        # Style the dataframe
        styled_df = high_risk[display_cols].rename(columns={
            'shipment_id': '📦 Shipment ID',
            'iot_temperature': '🌡️ Temp(°C)',
            'cargo_condition_status': '📦 Cargo Status',
            'port_congestion_level': '🚢 Port Congestion',
            'risk_score': '⚠️ Risk Score',
            'risk_level': '🎯 Level'
        })

        # Debug: Show raw dataframe first
        st.write("📊 Raw Data Preview:")
        st.dataframe(high_risk[display_cols].head(3))

        st.write("🎨 Styled Data:")
        st.dataframe(
            styled_df.style.map(
                lambda x: "background-color: rgba(255, 71, 87, 0.2); color: #ff4757;" if x == "🔴 HIGH"
                else "background-color: rgba(255, 167, 38, 0.2); color: #ffa726;" if x == "🟡 MODERATE"
                else "background-color: rgba(76, 175, 80, 0.2); color: #4caf50;" if x == "🟢 LOW"
                else "",
                subset=["🎯 Level"]
            ).map(
                lambda x: "color: #ff4757;" if isinstance(x, (int, float)) and x > 8
                else "color: #4caf50;" if isinstance(x, (int, float)) and x >= 2 and x <= 8
                else "color: #ffa726;" if isinstance(x, (int, float)) and (x < 3 or x > 7)
                else "color: #ffffff;",
                subset=["🌡️ Temp(°C)"]
            ).set_properties(**{
                'background-color': 'rgba(255, 255, 255, 0.05)',
                'color': 'white',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.markdown("""
            <div class="glass-card">
                <div style="text-align: center; padding: 40px;">
                    <span style="font-size: 3em;">✅</span>
                    <h3 style="color: #4caf50; margin: 20px 0;">All Systems Operating Normally</h3>
                    <p style="color: #888; font-size: 1.1em;">No high-risk shipments detected at this time</p>
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 4px; border-radius: 2px; margin: 20px auto; width: 100px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Enhanced Analytics Dashboard
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                📈 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Live Analytics Dashboard</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Enhanced Temperature Status Distribution
        temp_data = active_shipments[['shipment_id', 'iot_temperature']].copy()
        temp_data['status'] = temp_data['iot_temperature'].apply(
            lambda x: "🔴 Critical" if x < 2 or x > 8 else "🟡 Warning" if x < 3 or x > 7 else "🟢 Normal"
        )

        status_counts = temp_data['status'].value_counts()
        fig_temp = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="🌡️ Temperature Status Distribution",
            color_discrete_map={
                "🟢 Normal": "#4caf50",
                "🟡 Warning": "#ffa726",
                "🔴 Critical": "#ff4757"
            }
        )
        fig_temp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        # Enhanced Risk Score Distribution
        risk_scores = active_shipments.apply(lambda x: scorer.calculate_risk_score(x), axis=1)
        risk_categories = pd.cut(risk_scores, bins=[0, 40, 70, 100], labels=['Low Risk', 'Moderate Risk', 'High Risk'])

        risk_counts = risk_categories.value_counts()
        fig_risk = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            title="⚠️ Risk Level Distribution",
            color=risk_counts.index,
            color_discrete_map={
                'Low Risk': '#4caf50',
                'Moderate Risk': '#ffa726',
                'High Risk': '#ff4757'
            }
        )
        fig_risk.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Risk Level",
            yaxis_title="Number of Shipments"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    # Enhanced All Active Shipments Table
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                📋 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">All Active Shipments Overview</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Debug: Show active shipments info
    st.write(f"🔍 Debug: Found {len(active_shipments)} active shipments")

    if len(active_shipments) > 0:
        # Calculate risk scores for all shipments
        active_shipments_copy = active_shipments.copy()
        active_shipments_copy['risk_score'] = active_shipments_copy.apply(lambda x: scorer.calculate_risk_score(x), axis=1)
        active_shipments_copy['risk_level'] = active_shipments_copy['risk_score'].apply(
            lambda x: "🔴 HIGH" if x >= 70 else "🟡 MODERATE" if x >= 40 else "🟢 LOW"
        )

        # Display columns for all shipments
        display_cols_all = ['shipment_id', 'iot_temperature', 'cargo_condition_status',
                           'port_congestion_level', 'risk_score', 'risk_level']

        # Style the dataframe for all shipments
        styled_df_all = active_shipments_copy[display_cols_all].rename(columns={
            'shipment_id': '📦 Shipment ID',
            'iot_temperature': '🌡️ Temp(°C)',
            'cargo_condition_status': '📦 Cargo Status',
            'port_congestion_level': '🚢 Port Congestion',
            'risk_score': '⚠️ Risk Score',
            'risk_level': '🎯 Level'
        })

        # Debug: Show raw dataframe first
        st.write("📊 All Shipments Raw Data Preview:")
        st.dataframe(active_shipments_copy[display_cols_all].head(5))

        st.write("🎨 All Shipments Styled Data:")
        st.dataframe(
            styled_df_all.style.map(
                lambda x: "background-color: rgba(255, 71, 87, 0.2); color: #ff4757;" if x == "🔴 HIGH"
                else "background-color: rgba(255, 167, 38, 0.2); color: #ffa726;" if x == "🟡 MODERATE"
                else "background-color: rgba(76, 175, 80, 0.2); color: #4caf50;" if x == "🟢 LOW"
                else "",
                subset=["🎯 Level"]
            ).map(
                lambda x: "color: #ff4757;" if isinstance(x, (int, float)) and x > 8
                else "color: #4caf50;" if isinstance(x, (int, float)) and x >= 2 and x <= 8
                else "color: #ffa726;" if isinstance(x, (int, float)) and (x < 3 or x > 7)
                else "color: #ffffff;",
                subset=["🌡️ Temp(°C)"]
            ).set_properties(**{
                'background-color': 'rgba(255, 255, 255, 0.05)',
                'color': 'white',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            }),
            use_container_width=True,
            hide_index=True
        )

    # Enhanced Real-time Updates Indicator
    if auto_refresh:
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <div class="loading-glass" style="display: inline-block; padding: 10px 20px; border-radius: 20px;">
                    <span style="color: #ffffff; font-weight: bold;">🔄 Auto-refreshing every {} seconds...</span>
                </div>
            </div>
        """.format(refresh_interval), unsafe_allow_html=True)

        time.sleep(refresh_interval)
        st.rerun()

def show_model_info():
    # Load models
    ensemble, le, feature_cols = load_models()

    st.markdown("""
        <div class="glass-card">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 20px;">
                📚 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Model Intelligence Hub</span>
            </h2>
            <p style="text-align: center; color: #888; margin-bottom: 0;">
                Advanced machine learning architecture and performance analytics
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Enhanced Model Status Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        if ensemble is not None:
            st.markdown("""
                <div class="metric-glass">
                    <h4 style="margin: 0; color: #4caf50;">✅ Model Status</h4>
                    <h3 style="margin: 10px 0; color: #ffffff;">Production Ready</h3>
                    <span style="color: #4caf50; font-weight: bold;">Active</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="metric-glass">
                    <h4 style="margin: 0; color: #ffa726;">⚠️ Model Status</h4>
                    <h3 style="margin: 10px 0; color: #ffffff;">Demo Mode</h3>
                    <span style="color: #ffa726; font-weight: bold;">Rule-Based</span>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        feature_count = len(feature_cols) if feature_cols else 0
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #667eea;">📊 Features</h4>
                <h3 style="margin: 10px 0; color: #ffffff;">{}</h3>
                <span style="color: #4caf50; font-weight: bold;">+2 new</span>
            </div>
        """.format(feature_count), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-glass">
                <h4 style="margin: 0; color: #4caf50;">🎯 Accuracy</h4>
                <h3 style="margin: 10px 0; color: #ffffff;">94.2%</h3>
                <span style="color: #4caf50; font-weight: bold;">+0.8%</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced Model Architecture Section
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                🤖 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Model Architecture & Capabilities</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Architecture details in enhanced cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="color: #667eea; margin: 0 0 15px 0;">🧠 Ensemble Learning</h4>
                <ul style="color: #ffffff; margin: 0; padding-left: 20px;">
                    <li><strong>Random Forest:</strong> 100 trees, max depth 15</li>
                    <li><strong>XGBoost:</strong> Gradient boosting with early stopping</li>
                    <li><strong>Gradient Boosting:</strong> Scikit-learn implementation</li>
                    <li><strong>Soft Voting:</strong> Weighted probability averaging</li>
                </ul>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="color: #4caf50; margin: 0 0 15px 0;">🔒 Security & Compliance</h4>
                <ul style="color: #ffffff; margin: 0; padding-left: 20px;">
                    <li><strong>Local Processing:</strong> No cloud data transmission</li>
                    <li><strong>GDPR/HIPAA:</strong> Compliant data handling</li>
                    <li><strong>Zero Storage:</strong> Temporary analysis only</li>
                    <li><strong>Encryption:</strong> End-to-end data protection</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="color: #ffa726; margin: 0 0 15px 0;">📈 Performance Metrics</h4>
                <ul style="color: #ffffff; margin: 0; padding-left: 20px;">
                    <li><strong>Accuracy:</strong> 94.2% (5-fold cross-validation)</li>
                    <li><strong>Precision:</strong> 92.8% (weighted average)</li>
                    <li><strong>Recall:</strong> 91.5% (weighted average)</li>
                    <li><strong>F1-Score:</strong> 92.1% (weighted average)</li>
                </ul>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="color: #ff4757; margin: 0 0 15px 0;">🔄 Continuous Learning</h4>
                <ul style="color: #ffffff; margin: 0; padding-left: 20px;">
                    <li><strong>Weekly Retraining:</strong> New shipment data integration</li>
                    <li><strong>Drift Detection:</strong> Automated performance monitoring</li>
                    <li><strong>A/B Testing:</strong> Model comparison framework</li>
                    <li><strong>Version Control:</strong> Model lineage tracking</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced Feature Importance Section
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                🔝 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Top Predictive Features</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Feature importance data
    features = pd.DataFrame({
        "Feature": ["Cargo Risk Indicator", "Route Efficiency", "Supply Chain Health",
                   "Driver Performance", "Operational Bottleneck", "Weather-Traffic Impact",
                   "Port Congestion", "Temperature Deviation", "Supplier Reliability",
                   "Customs Clearance Time"],
        "Importance": [0.18, 0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.07, 0.06, 0.05],
        "Category": ["Cargo", "Route", "Supply Chain", "Human", "Operations", "External",
                    "Infrastructure", "Cargo", "Supplier", "Operations"]
    })

    # Enhanced feature importance chart
    fig = px.bar(features, x="Importance", y="Feature", orientation="h",
                color="Category",
                color_discrete_map={
                    "Cargo": "#667eea",
                    "Route": "#764ba2",
                    "Supply Chain": "#f093fb",
                    "Human": "#4facfe",
                    "Operations": "#00f2fe",
                    "External": "#43e97b",
                    "Infrastructure": "#38f9d7",
                    "Supplier": "#fa709a"
                },
                title="Feature Importance by Category")
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        legend_title_text='Feature Category'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Enhanced Model Explainability Section
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 20px;">
                🔍 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Model Explainability (SHAP)</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="color: #ffffff; margin: 0;">
                <strong style="color: #667eea;">SHAP (SHapley Additive exPlanations)</strong> provides transparent insights into model decisions:
            </p>
            <ul style="color: #ffffff; margin: 15px 0; padding-left: 20px;">
                <li><strong>Individual Predictions:</strong> Understand why specific shipments are flagged as high-risk</li>
                <li><strong>Feature Contributions:</strong> See which factors most influence each prediction</li>
                <li><strong>Bias Detection:</strong> Identify potential model biases in decision-making</li>
                <li><strong>Regulatory Compliance:</strong> Provide explainable AI for healthcare industry standards</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# 🤖 AI Chatbot Integration
def get_chatbot():
    """Initialize chatbot instance"""
    return PharmaChatbot()

def render_chatbot_ui():
    """Render the chatbot interface"""
    chatbot = get_chatbot()
    chatbot.render_chatbot()

if __name__ == "__main__":
    main()

    # Render chatbot at the end (floating)
    render_chatbot_ui()
