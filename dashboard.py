import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def main():
    # ---------------- UI STYLING & FULL SCREEN FIX ----------------
    st.markdown("""
    <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
            padding-top: 1.5rem !important;
        }

        .stApp { background-color: #0d1b2a !important; }
        header, [data-testid="stHeader"] { background-color: #0d1b2a !important; }
        
        /* Force Tabs to take full width and align across the top */
        [data-testid="stTabPanel"] {
            width: 100% !important;
        }

        .cyan-title {
            color: #4cc9f0 !important;
            font-weight: 800;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        /* TAB STYLING: White to Cyan Hover */
        button[data-baseweb="tab"] p {
            color: white !important;
            transition: 0.3s;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"]:hover p {
            color: #4cc9f0 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #4cc9f0 !important;
        }

        .kpi-card {
            background-color: #1b263b;
            border: 1px solid #415a77;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .kpi-label { color: #778da9; font-size: 12px; font-weight: 600; }
        .kpi-value { color: white; font-size: 24px; font-weight: 800; }

        div.stButton > button {
            background-color: #4cc9f0 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            width: 100%;
        }
        
        div.stButton > button:hover {
            background-color: #ffffff !important;
            color: #4cc9f0 !important;
        }

        .insight-box {
            background-color: #1b263b;
            border-left: 5px solid #4cc9f0;
            padding: 20px;
            border-radius: 0 12px 12px 0;
            color: white;
            margin-top: 10px;
            width: 100% !important;
        }

        .white-edu-text { color: #ffffff !important; font-size: 16px; line-height: 1.6; }
        .white-bullets li { color: #ffffff !important; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- DATA FETCHING ----------------
    @st.cache_data(ttl=300)
    def fetch_real_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-bAm69cGY5PQKTQBY8HM82bwf"}
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 25, "sparkline": "true", "price_change_percentage": "24h"}
        try:
            response = requests.get(url, params=params, headers=headers)
            return response.json() if response.status_code == 200 else []
        except: return []

    def get_risk_info(change):
        abs_change = abs(change or 0)
        if abs_change > 5: return "HIGH", "#ef476f"
        if abs_change > 2: return "MEDIUM", "#ffd166"
        return "LOW", "#06d6a0"

    data = fetch_real_data()

    # ---------------- NAVBAR ----------------
    tab_home, tab_about, tab_risk, tab_reports, tab_settings, tab_contact = st.tabs([
        "🏠 HOME", "📖 ABOUT", "📊 RISK ANALYTICS", "📑 REPORTS", "⚙️ SETTINGS", "📞 CONTACT"
    ])

    with tab_home:
        # Header Row
        head_left, head_right = st.columns([5, 1])
        with head_left:
            st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
        with head_right:
            if st.button("🚪 LOGOUT"):
                st.session_state.authenticated = False
                st.rerun()

        st.write("---")
        if not data:
            st.warning("⚠️ API connection busy. Please wait a moment.")
            st.stop()

        # KPI ROW
        total_coins = len(data)
        high_risk_assets = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5]
        high_risk = len(high_risk_assets)
        low_risk = len([c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= 2])
        risk_exp = (high_risk / total_coins) * 100 if total_coins > 0 else 0

        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        sum_col1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Assets</div><div class='kpi-value'>{total_coins}</div></div>", unsafe_allow_html=True)
        sum_col2.markdown(f"<div class='kpi-card'><div class='kpi-label'>High Risk</div><div class='kpi-value' style='color:#ef476f;'>{high_risk}</div></div>", unsafe_allow_html=True)
        sum_col3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Low Risk</div><div class='kpi-value' style='color:#06d6a0;'>{low_risk}</div></div>", unsafe_allow_html=True)
        sum_col4.markdown(f"<div class='kpi-card'><div class='kpi-label'>Risk Exposure</div><div class='kpi-value' style='color:#4cc9f0;'>{risk_exp:.1f}%</div></div>", unsafe_allow_html=True)

        st.write("")
        col_t, col_r = st.columns([5, 1])
        col_t.markdown("<div class='cyan-title'>📋 Market Risk Monitor </div>", unsafe_allow_html=True)
        if col_r.button("🔄 REFRESH"):
            st.cache_data.clear()
            st.rerun()

        # TABLE
        table_rows = ""
        for coin in data:
            change = coin.get('price_change_percentage_24h', 0) or 0
            risk_text, risk_color = get_risk_info(change)
            change_color = "#06d6a0" if change >= 0 else "#ef476f"
            table_rows += f"""<tr style="border-bottom: 1px solid #2b3a4f;"><td style="padding:14px;"><img src="{coin.get('image', '')}" width="22" style="vertical-align:middle;margin-right:12px;"><b>{coin.get('name')}</b></td><td style="padding:14px; font-family:monospace;">${coin.get('current_price', 0):,}</td><td style="padding:14px; color:{change_color}; font-weight:bold;">{change:.2f}%</td><td style="padding:14px;"><span style="background:{risk_color}; color:#0d1b2a; padding:3px 10px; border-radius:4px; font-weight:900; font-size:10px;">{risk_text}</span></td><td style="padding:14px; text-align:right; color:#4cc9f0; font-size:12px;">LIVE</td></tr>"""

        full_table_html = f"""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif; color:white;"><div style="max-height: 400px; overflow-y: auto;"><table style="width:100%; border-collapse:collapse; text-align:left;"><thead style="position: sticky; top: 0; background: #4cc9f0; z-index: 10;"><tr style="color:white; font-size:12px; letter-spacing:1px; font-weight:bold;"><th style="padding:15px;">CRYPTO CURRENCIES</th><th style="padding:15px;">PRICE (USD)</th><th style="padding:15px;">24H CHANGE</th><th style="padding:15px;">RISK STATUS</th><th style="padding:15px; text-align:right;">STATUS</th></tr></thead><tbody>{table_rows}</tbody></table></div></div>"""
        components.html(full_table_html, height=450)
        
        st.write("---")
        # CHARTS
        col_a, col_b = st.columns([1.2, 1])
        with col_a:
            st.markdown("<div class='cyan-title'>📊 Demand & Price Trend</div>", unsafe_allow_html=True)
            coin_names = [c.get('name') for c in data]
            selected_coin = st.selectbox("SELECT ASSET", coin_names)
            coin_obj = next((c for c in data if c.get('name') == selected_coin), None)
            if coin_obj and 'sparkline_in_7d' in coin_obj:
                y_data = coin_obj['sparkline_in_7d']['price']
                fig_t = go.Figure()
                fig_t.add_trace(go.Scatter(y=y_data, mode='lines', line=dict(color='#4cc9f0', width=3), fill='tozeroy', fillcolor='rgba(76, 201, 240, 0.1)'))
                fig_t.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40))
                st.plotly_chart(fig_t, use_container_width=True)

    with tab_about:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>🚀 About the Project</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">This system analyzes cryptocurrency volatility to estimate risk levels. It fetches data via CoinGecko/Binance APIs and performs quantitative analysis.</p>', unsafe_allow_html=True)
        # Interactive table or cards can be added here as previously defined.

    with tab_risk:
        st.markdown("<h2 style='color:#4cc9f0;'>📊 Quantitative Risk Analytics</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">This module focuses on <b>Milestone 2</b>: Computing Sharpe Ratio and Beta Coefficients for volatility benchmarking.</p>', unsafe_allow_html=True)
        st.info("Mathematical models for Daily and Annualized Volatility are being integrated into the backend.")

    with tab_reports:
        st.markdown("<h2 style='color:#4cc9f0;'>📑 Export & Generation</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">Generate comprehensive risk reports in PDF or CSV format for the selected assets.</p>', unsafe_allow_html=True)
        st.button("📥 DOWNLOAD MARKET SUMMARY (PDF)")

    with tab_settings:
        st.markdown("<h2 style='color:#4cc9f0;'>⚙️ Market Settings</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">Adjust system parameters for risk calculation and display preferences.</p>', unsafe_allow_html=True)
        st.selectbox("Default Currency", ["USD ($)", "EUR (€)", "INR (₹)"])
        st.slider("Volatility Lookback Period (Days)", 7, 30, 7)

    with tab_contact:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>📞 Contact Support</h2>", unsafe_allow_html=True)
        st.markdown('<div class="insight-box"><b>Developer Support:</b> support@cryptorisk.com<br><b>Location:</b> Nagpur, MH</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
