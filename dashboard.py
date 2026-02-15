import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def main():
    # ---------------- UI STYLING ----------------
    st.markdown("""
    <style>
        .stApp { background-color: #0d1b2a !important; }
        
        /* 1. STICKY NAVBAR STYLING */
        .nav-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #0d1b2a;
            border-bottom: 2px solid #4cc9f0;
            padding: 10px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 9999;
        }
        .nav-links { display: flex; gap: 25px; }
        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            transition: 0.3s;
        }
        .nav-links a:hover { color: #4cc9f0; }

        /* 2. ATTRACTIVE SECTION OVERLAYS */
        .glass-panel {
            background: rgba(27, 38, 59, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid #415a77;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
        }

        .cyan-title {
            color: #4cc9f0 !important;
            font-weight: 800;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        /* 3. SOLID CYAN BUTTONS */
        div.stButton > button {
            background-color: #4cc9f0 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            text-decoration: none !important;
        }
        
        div.stButton > button:hover {
            background-color: #ffffff !important;
            color: #4cc9f0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- NAVIGATION LOGIC ----------------
    # Create navigation links in a sidebar-style or top-menu selector
    st.markdown("""
        <div class="nav-container">
            <div style="color: #4cc9f0; font-weight: 800; font-size: 18px;">CRYPTO ANALYZER</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Adding tabs for the navbar links you requested
    tabs = st.tabs(["🏠 HOME", "📊 ANALYSIS", "ℹ️ ABOUT", "📞 CONTACT"])

    # ---------------- TAB 1: HOME (YOUR MAIN DASHBOARD) ----------------
    with tabs[0]:
        # Header with Logout
        head_left, head_right = st.columns([5, 1])
        with head_left:
            st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
        with head_right:
            if st.button("🚪 LOGOUT", key="logout_btn"):
                st.session_state.authenticated = False
                st.rerun()

        # Fetch Data
        @st.cache_data(ttl=300)
        def fetch_real_data():
            url = "https://api.coingecko.com/api/v3/coins/markets"
            headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-bAm69cGY5PQKTQBY8HM82bwf"}
            params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 25, "sparkline": "true"}
            try:
                response = requests.get(url, params=params, headers=headers)
                return response.json() if response.status_code == 200 else []
            except: return []

        data = fetch_real_data()

        if not data:
            st.warning("⚠️ API connection busy. Please wait a moment.")
        else:
            # KPI Row
            total_coins = len(data)
            sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
            sum_col1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Assets</div><div class='kpi-value'>{total_coins}</div></div>", unsafe_allow_html=True)
            # (Rest of your KPI calculations here...)

            # Market Monitor Table
            st.markdown("<div class='cyan-title'>📋 Market Risk Monitor </div>", unsafe_allow_html=True)
            # (Insert your full Table HTML here...)

    # ---------------- TAB 2: ANALYSIS (BASED ON PDF MODULES) ----------------
    with tabs[1]:
        st.markdown("<h1 class='cyan-title'>📊 Risk Calculation Module</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-panel">
            <p style="color:white;">As per <b>Milestone 2</b>, this module focuses on:</p>
            <ul style="color: #778da9;">
                [cite_start]<li>Calculating <b>Sharpe Ratio</b> and <b>Beta Coefficients</b>[cite: 15, 31].</li>
                [cite_start]<li>Implementing <b>Rolling Window Volatility</b>[cite: 32, 102].</li>
                [cite_start]<li>Deriving Value-at-Risk (VaR) measurements[cite: 31, 118].</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        # Add your Charts Section here for a perfect look

    # ---------------- TAB 3: ABOUT (ATTRACTIVE OVERLAY) ----------------
    with tabs[2]:
        st.markdown("<h1 class='cyan-title'>ℹ️ Project Statement</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-panel">
            <p style="color: white; font-size: 16px; line-height: 1.6;">
                The <b>Crypto Volatility and Risk Analyzer</b> project aims to analyze and visualize the volatility 
                [cite_start]patterns of selected cryptocurrencies to estimate their risk levels over time[cite: 7]. 
                By fetching real-time data from <b>CoinGecko</b>, the system performs quantitative analysis to measure 
                [cite_start]market health and decision-support trade-offs[cite: 8, 21].
            </p>
            <hr style="border: 0.5px solid #415a77;">
            <p style="color: #4cc9f0; font-weight: 700;">CORE OUTCOMES:</p>
            [cite_start]<span style="color: #778da9;">• Dynamic Data Fetching [cite: 12][cite_start]<br>• Risk Categorization [cite: 18][cite_start]<br>• Interactive Visual Dashboards [cite: 16]</span>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 4: CONTACT US (ATTRACTIVE FORM) ----------------
    with tabs[3]:
        st.markdown("<h1 class='cyan-title'>📞 Get In Touch</h1>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
            <div class="glass-panel">
                <b style="color:#4cc9f0;">DEVELOPMENT HUB</b><br>
                <p style="color:white; font-size: 14px;">Nagpur, Maharashtra, India<br>
                Email: support@cryptoanalyzer.io<br>
                [cite_start]Status: System Live Analysis [cite: 111]</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            with st.form("contact_form"):
                st.text_input("Name", placeholder="Enter your name")
                st.text_input("Email", placeholder="Enter your email")
                st.text_area("Message", placeholder="How can we help you?")
                st.form_submit_button("SEND MESSAGE")

if __name__ == "__main__":
    main()
