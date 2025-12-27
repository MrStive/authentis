
import streamlit as st

def apply_custom_style():
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        :root {
            --primary-color: #6366f1; /* Indigo */
            --secondary-color: #a855f7; /* Purple */
            --background-dark: #0f172a;
            --surface-dark: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }

        /* App Background */
        .stApp {
            background-color: var(--background-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
        }

        /* Sidebar Styling */
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: var(--surface-dark);
            border-right: 1px solid var(--glass-border);
        }

        /* Sidebar Navigation Items */
        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebarNav"] a {
            color: var(--text-secondary);
            font-weight: 500;
            padding: 0.5rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            text-decoration: none;
        }

        [data-testid="stSidebarNav"] a:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(4px);
        }

        /* Active Navigation Item (approximate selector for Streamlit) */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(99, 102, 241, 0.15); /* Primary color low opacity */
            color: var(--primary-color) !important;
            border-left: 3px solid var(--primary-color);
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.5rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--glass-border);
        }

        [data-testid="stSidebar"] .stMarkdown {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* Typography */
        h1, h2, h3 {
            color: var(--text-primary) !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        p, label, .stMarkdown {
            color: var(--text-secondary) !important;
            line-height: 1.6;
        }

        /* Metrics / Cards */
        [data-testid="stMetric"] {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: var(--primary-color);
        }
        
        [data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
            font-size: 0.9rem;
        }
        
        [data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
            font-weight: 700;
        }

        /* Buttons */
        .stButton button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.23) !important;
            filter: brightness(1.1);
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            overflow: hidden;
        }

        /* Custom Cards */
        .feature-card {
            background: var(--surface-dark);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 24px;
            height: 100%;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-4px);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            line-height: 1.2;
        }

        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)
