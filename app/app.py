
import streamlit as st
import pandas as pd
import sys
import os

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.style import apply_custom_style

st.set_page_config(
    page_title="Marketing Analytics Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Global CSS
apply_custom_style()

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.info("Select a page above to explore the dashboard.")

# --- Hero Section ---
st.markdown('<h1 class="hero-title">Marketing Analytics<br>Intelligence Engine</h1>', unsafe_allow_html=True)
st.markdown("<h4>Automate analysis, predict retention, and optimize ROI with AI-driven insights.</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Feature Grid ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Real-time Dashboard</h3>
        <p>monitor executive KPIs, revenue trends, and operational metrics in real-time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔮</div>
        <h3>Predictive AI</h3>
        <p>Forecast Customer Lifetime Value (LTV) and detect churn risks before they happen.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <h3>Advanced Segmentation</h3>
        <p>Cluster customers using RFM analysis and behavioral patterns for targeted campaigns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Automated Reporting</h3>
        <p>Generate production-ready PDF & PPTX strategy reports with a single click.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- System Status ---
st.subheader("System Status")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown('<div>Pipeline <span class="status-badge">✅ Active</span></div>', unsafe_allow_html=True)
with col_s2:
    st.markdown('<div>Models <span class="status-badge">✅ Trained</span></div>', unsafe_allow_html=True)
with col_s3:
     st.markdown(f'<div>Last Update <span class="status-badge">{pd.Timestamp.now().strftime("%H:%M")}</span></div>', unsafe_allow_html=True)


# Load data check (hidden or subtle)
try:
    df = pd.read_csv('data/processed/marketing_analysis.csv')
    # Optional: could show a small toast or just keep it silent if working
    # st.toast(f"System connected: {len(df)} records.", icon="🟢")
except FileNotFoundError:
    st.warning("Processed data not found. Please run the analysis pipeline.")
