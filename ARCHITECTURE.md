# Architecture Documentation: Marketing Analytics Software

## Overview

This system is a data-driven marketing analysis platform designed to process synthetic customer data, perform advanced segmentation (RFM + K-Means), and visualize insights via an interactive dashboard.

## System Architecture

### 1. Data Layer

- **Source**: Synthetic Generation (`src/data_generation/generate_data.py`).
- **Raw Data**: `data/raw/marketing_data.csv` (5,000 records).
- **Processing**: `src/analysis/perform_analysis.py`.
- **Storage**: `data/processed/marketing_analysis.csv`.

### 2. Analysis Pipeline

- **RFM Scoring**: Recency, Frequency, Monetary quintiles (1-5).
- **Clustering**: K-Means with standard scaling and elbow method (k=5).
- **Labeling Logic**:
  - _Champions_: High R, F, M.
  - _Loyal_: High F, Mid-High R/M.
  - _Potential_: High R, Low F/M.
  - _Dormant_: Low R, F, M.
  - _At Risk_: Low R, High F/M.

### 3. Application Layer (Streamlit)

- **`app.py`**: Entry point and navigation.
- **Pages**:
  1.  **Dashboard**: Executive KPIs, Simulated Revenue Line, Map.
  2.  **Segmentation**: 3D Plotly Clusters, Filters, CSV Export.
  3.  **Predictions**: LTV Calculator, Churn Detection, Campaign ROI Simulator.
  4.  **Reporting**: Automated PPTX and Markdown Report generation.

## Key Technologies

- **Python 3.12**
- **Pandas/NumPy**: Data manipulation.
- **Scikit-Learn**: Clustering (K-Means).
- **Streamlit**: Web Interface.
- **Plotly**: Interactive Visualizations.
- **Python-PPTX**: Report Generation.

## Usage

1.  **Generate Data**: `python src/data_generation/generate_data.py`
2.  **Run Analysis**: `python src/analysis/perform_analysis.py`
3.  **Launch App**: `streamlit run app/app.py`
