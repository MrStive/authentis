
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.style import apply_custom_style

st.set_page_config(page_title="Segmentation & Clustering", page_icon="👥", layout="wide")
apply_custom_style()

st.title("👥 Segmentation Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/marketing_analysis.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data not found.")
    st.stop()

# --- Filters ---
st.sidebar.header("Filters")
selected_segments = st.sidebar.multiselect(
    "Select Segments", 
    options=df['Segment_Label'].unique(),
    default=df['Segment_Label'].unique()
)

filtered_df = df[df['Segment_Label'].isin(selected_segments)]

# --- 3D Visualization ---
st.subheader("Interactive 3D Customer Clusters")
st.info("Rotate, zoom, and hover to explore RFM clusters.")

# Sampling for performance if dataset is large, but 5000 is fine.
fig_3d = px.scatter_3d(
    filtered_df, 
    x='Recency', 
    y='Frequency', 
    z='Monetary',
    color='Segment_Label',
    hover_name='ClientID',
    hover_data=['Age', 'Location'],
    opacity=0.7,
    title="3D View: Recency vs Frequency vs Monetary"
)
fig_3d.update_layout(height=600)
st.plotly_chart(fig_3d, use_container_width=True)

# --- Segment Statistics ---
st.markdown("---")
st.subheader("Segment Deep-Dive")

stats = filtered_df.groupby('Segment_Label').agg({
    'ClientID': 'count',
    'MontantTotalDepense': 'mean',
    'FrequenceAchats': 'mean',
    'Recency': 'mean',
    'ScoreSatisfaction': 'mean'
}).reset_index()

stats.columns = ['Segment', 'Profiles', 'Avg Spend (€)', 'Avg Freq', 'Avg Recency (Days)', 'Avg Satisfaction']
st.dataframe(stats.style.background_gradient(cmap="Blues"), use_container_width=True)

# --- Detailed Look & Export ---
st.markdown("---")
st.subheader("Detailed Profiles")

col1, col2 = st.columns([3, 1])
with col1:
    st.dataframe(filtered_df.drop(columns=['R_Score', 'F_Score', 'M_Score', 'RFM_Segment', 'Cluster']), height=300)

with col2:
    st.write("### Actions")
    st.write("Export the currently filtered list for email marketing campaigns.")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export to CSV",
        data=csv,
        file_name='segmented_customers.csv',
        mime='text/csv',
    )
    
    st.info(f"Exporting {len(filtered_df)} profiles.")
