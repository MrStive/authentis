
import streamlit as st
import pandas as pd
import io
import sys
import os

# Put root dir in path BEFORE importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.connectors import GA4Connector, SQLConnector
from utils.style import apply_custom_style

st.set_page_config(page_title="Data Connectivity", page_icon="📥", layout="wide")
apply_custom_style()

st.title("📥 Data Connectivity & Import")
st.markdown("Connect your real-world data sources or upload files to power the analysis.")

if 'data_source' not in st.session_state:
    st.session_state['data_source'] = 'Synthetic'

st.info(f"Current Data Source: **{st.session_state['data_source']}**")

# Tabs
tab_files, tab_manual, tab_connectors = st.tabs(["📂 File Import", "✍️ Manual Entry", "🔌 Connectors"])

# --- Tab 1: File Import ---
with tab_files:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'parquet'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.parquet'):
                df = pd.read_parquet(uploaded_file)
            
            st.success(f"Loaded {len(df)} rows from {uploaded_file.name}")
            st.dataframe(df.head())
            
            if st.button("Use this Data for Analysis"):
                # Save to processed path or session state
                # For this architecture, we overwrite the processed file or set a session variable.
                # Overwriting is dangerous but simplest for this demo.
                # Ideally, we map columns first.
                
                required_cols = ['ClientID', 'MontantTotalDepense', 'FrequenceAchats', 'DateDernierAchat']
                missing = [c for c in required_cols if c not in df.columns]
                
                if missing:
                    st.error(f"Missing required columns for analysis: {missing}")
                else:
                    target_path = 'data/processed/marketing_analysis.csv'
                    # We might need to run analysis pipeline on this new data?
                    # For now, just save it and assume it's pre-processed or compatible.
                    df.to_csv(target_path, index=False)
                    st.session_state['data_source'] = f"File: {uploaded_file.name}"
                    st.success("Data activated! Go to Dashboard or Analysis pages.")
                    
        except Exception as e:
            st.error(f"Error loading file: {e}")

# --- Tab 2: Manual Entry ---
with tab_manual:
    st.header("Manual Data Entry")
    st.markdown("Edit or add records manually.")
    
    # Load current data (or empty template)
    try:
        current_df = pd.read_csv('data/processed/marketing_analysis.csv')
    except:
        current_df = pd.DataFrame(columns=['ClientID', 'MontantTotalDepense', 'FrequenceAchats'])
    
    edited_df = st.data_editor(current_df, num_rows="dynamic")
    
    if st.button("Save Changes"):
        edited_df.to_csv('data/processed/marketing_analysis.csv', index=False)
        st.success("Changes saved successfully!")

# --- Tab 3: Connectors ---
with tab_connectors:
    st.header("External Date Connectors")
    
    conn_type = st.selectbox("Select Connector", ["Google Analytics 4", "PostgreSQL Database", "Meta Ads (Coming Soon)"])
    
    if conn_type == "Google Analytics 4":
        st.subheader("GA4 Configuration")
        prop_id = st.text_input("Property ID")
        creds_file = st.file_uploader("Service Account JSON", type=['json'])
        
        if st.button("Connect & Fetch GA4"):
            if not prop_id: # or not creds_file
                 st.error("Please provide Property ID (and credentials in env).")
            else:
                # Mock config
                config = {'property_id': prop_id}
                connector = GA4Connector(config)
                if connector.connect():
                    st.success("Connected to GA4!")
                    # In real app: fetch data
                else:
                    st.error("Connection Failed.")
                    
    elif conn_type == "PostgreSQL Database":
        st.subheader("Database Configuration")
        conn_str = st.text_input("Connection String (sqlalchemy format)", value="postgresql://user:password@localhost:5432/marketing_db")
        query = st.text_area("SQL Query", value="SELECT * FROM customers")
        
        if st.button("Import from SQL"):
            connector = SQLConnector({'connection_string': conn_str})
            if connector.connect():
                df_sql = connector.fetch_data(query)
                if not df_sql.empty:
                    st.success(f"Fetched {len(df_sql)} rows.")
                    st.dataframe(df_sql.head())
                    # Logic to Map and Save...
                else:
                    st.warning("No data returned.")
            else:
                st.error("Connection failed.")

