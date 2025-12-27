
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.style import apply_custom_style

st.set_page_config(page_title="Predictions & Simulations", page_icon="🔮", layout="wide")
apply_custom_style()

st.title("🔮 Predictions & Simulations")

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/marketing_analysis.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data not found.")
    st.stop()

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["LTV Calculator", "Churn Risk", "Campaign Simulator"])

# --- Tab 1: LTV Calculator ---
with tab1:
    st.header("LTV Calculator (New Customer)")
    st.markdown("Estimate the Lifetime Value of a new customer based on initial signals.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Customer Age", 18, 75, 30)
        channel = st.selectbox("Acquisition Channel", ['Social', 'Email', 'SEA', 'Direct', 'Reference'])
        first_basket = st.number_input("First Basket Value (€)", min_value=10.0, value=50.0)
    
    with col2:
        # Dummy logic for LTV prediction
        # Base LTV + Channel Multiplier + Basket Multiplier
        channel_mult = {'Social': 1.2, 'Email': 1.5, 'Reference': 1.8, 'SEA': 1.0, 'Direct': 1.1}
        est_ltv = first_basket * 3 * channel_mult.get(channel, 1.0) * (1 + (75-age)/100)
        
        st.metric("Estimated LTV (12 Months)", f"€{est_ltv:.2f}")
        st.info("Based on historical cohorts, similar profiles spend this amount over 12 months.")

# --- Tab 2: Churn Risk ---
with tab2:
    st.header("Churn Risk Detector")
    st.markdown("Identify customers with high probability of leaving.")
    
    risk_df = df[df['Segment_Label'] == 'A risque'].sort_values('Recency', ascending=False)
    
    st.warning(f"{len(risk_df)} customers identified as 'At Risk' (High RFM Churn Signal).")
    
    fig_risk = px.histogram(risk_df, x='Recency', title="Distribution of Days Since Last Purchase (At Risk Segment)")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.subheader("Top Risk Profiles")
    st.dataframe(risk_df[['ClientID', 'Recency', 'MontantTotalDepense', 'FrequenceAchats']].head(50), use_container_width=True)

# --- Tab 3: Campaign Simulator ---
with tab3:
    st.header("Campaign ROI Simulator")
    st.markdown("Simulate the impact of a retention campaign on the 'At Risk' segment.")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        target_revenue = risk_df['MontantTotalDepense'].sum()
        st.metric("Total Revenue at Risk", f"€{target_revenue:,.0f}")
        
        campaign_cost = st.number_input("Campaign Budget (€)", value=5000)
        conversion_rate = st.slider("Est. Conversion Rate (%)", 1, 20, 5)
        discount = st.slider("Discount Offer (%)", 0, 50, 10)
    
    with col_sim2:
        # Business Logic
        # Recovered Customers = Count * Conversion Rate
        # Recovered Revenue = Recovered Customers * Avg Spend * (1 - Discount)
        # ROI = (Recovered Revenue - Cost) / Cost
        
        recovered_customers = int(len(risk_df) * (conversion_rate/100))
        avg_spend = risk_df['MontantTotalDepense'].mean()
        recovered_revenue = recovered_customers * avg_spend * (1 - discount/100)
        roi = ((recovered_revenue - campaign_cost) / campaign_cost) * 100 if campaign_cost > 0 else 0
        
        st.metric("Recovered Customers", f"{recovered_customers}")
        st.metric("Recovered Revenue", f"€{recovered_revenue:,.0f}")
        st.metric("Campaign ROI", f"{roi:.1f}%", delta_color="normal" if roi > 0 else "inverse")
        
        if roi > 100:
            st.success("High ROI! Recommended campaign.")
        elif roi > 0:
            st.info("Positive ROI. Worth considering.")
        else:
            st.error("Negative ROI. Adjust budget or targeting.")
