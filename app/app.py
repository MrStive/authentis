
import streamlit as st
import pandas as pd
import sys
import os

# Add root to path so we can import from src if needed, 
# although we should rely on processed data.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="Marketing Analytics Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.info("Select a page above to explore the dashboard.")

st.title("🚀 Marketing Analytics Engine")
st.markdown("""
### Welcome to the Data-Driven Marketing Intelligence Suite.

This platform automates the analysis of your customer base, providing actionable insights to optimize ROI and retention.

**Modules:**
- **📊 Dashboard**: Real-time KPIs and Executive Summary.
- **👥 Segmentation**: Advanced RFM & Clustering Analysis.
- **🔮 Predictions**: LTV Forecasting and Churn Detection.
- **📈 Reporting**: Automated PDF/PPTX Strategy Reports.

---
**System Status**:
- Data Pipeline: ✅ Active
- Models: ✅ Trained
- Last Update: """ + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M") + """
""")

# Load data just to check status
try:
    df = pd.read_csv('data/processed/marketing_analysis.csv')
    st.success(f"Data Loaded Successfully: {len(df):,} records available.")
except FileNotFoundError:
    st.error("Processed data not found. Please run the analysis pipeline first.")
