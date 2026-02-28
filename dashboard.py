import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# IMPORT YOUR NEW MODULES
import data_processing as dp
import viz_dashboard as vz

def main():
    # --- STYLING (KEEP AS IS) ---
    st.markdown("""<style>
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; max-width: 100% !important; padding-top: 2rem !important; }
        .stApp { background-color: #0d1b2a !important; }
        header, [data-testid="stHeader"] { background-color: #0d1b2a !important; }
        [data-testid="stTabPanel"], [data-testid="stHorizontalBlock"] { width: 100% !important; }
        .cyan-title { color: #4cc9f0 !important; font-weight: 800; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }
        [data-testid="stWidgetLabel"] p { color: white !important; font-weight: 600 !important; }
        button[data-baseweb="tab"] p { color: white !important; transition: 0.3s; font-weight: 600 !important; }
        button[data-baseweb="tab"]:hover p { color: #4cc9f0 !important; }
        button[data-baseweb="tab"][aria-selected="true"] p { color: #4cc9f0 !important; }
        .kpi-card { background-color: #1b263b; border: 1px solid #415a77; padding: 15px; border-radius: 10px; text-align: center; }
        .kpi-label { color: #778da9; font-size: 12px; font-weight: 600; }
        .kpi-value { color: white; font-size: 24px; font-weight: 800; }
        div.stButton > button { background-color: #4cc9f0 !important; color: #ffffff !important; border: none !important; font-weight: 700 !important; border-radius: 6px !important; padding: 10px 20px !important; width: 100%; transition: 0.3s; }
        div.stButton > button:hover { background-color: #ffffff !important; color: #4cc9f0 !important; }
        .insight-box { background-color: #1b263b; border-left: 5px solid #4cc9f0; padding: 20px; border-radius: 0 12px 12px 0; color: white; margin-top: 10px; width: 100% !important; }
        .white-edu-text { color: #ffffff !important; font-size: 16px; line-height: 1.6; }
        .white-bullets li { color: #ffffff !important; margin-bottom: 12px; }
    </style>""", unsafe_allow_html=True)

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

    tab_data_acq, tab_about, tab_data_proc, tab_reports, tab_viz_dash, tab_risk_class, tab_contact = st.tabs([
        "📡 DATA ACQUISITION", "📖 ABOUT", "⚙️ DATA PROCESSING", "📑 REPORTS", "📊 VIZ DASHBOARD", "🛡️ RISK CLASSIFICATION", "📞 CONTACT"
    ])

    with tab_data_acq:
        head_left, head_right = st.columns([5, 1])
        with head_left: st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
        with head_right: 
            if st.button("🚪 LOGOUT", key="logout_acq"): st.rerun()

        st.write("---")
        if not data: st.warning("⚠️ API connection busy."); st.stop()

        total_coins = len(data)
        high_risk_assets = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5]
        high_risk = len(high_risk_assets)
        low_risk = len([c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= 2])
        risk_exp = (high_risk / total_coins) * 100 if total_coins > 0 else 0

        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        sum_col1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Coins</div><div class='kpi-value'>{total_coins}</div></div>", unsafe_allow_html=True)
        sum_col2.markdown(f"<div class='kpi-card'><div class='kpi-label'>High Risk</div><div class='kpi-value' style='color:#ef476f;'>{high_risk}</div></div>", unsafe_allow_html=True)
        sum_col3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Low Risk</div><div class='kpi-value' style='color:#06d6a0;'>{low_risk}</div></div>", unsafe_allow_html=True)
        sum_col4.markdown(f"<div class='kpi-card'><div class='kpi-label'>Risk Exposure</div><div class='kpi-value' style='color:#4cc9f0;'>{risk_exp:.1f}%</div></div>", unsafe_allow_html=True)

        st.write("")
        t_col_empty, t_col_right = st.columns([1, 1])
        with t_col_right:
            st.markdown("<div class='cyan-title'>📋 Market Risk Monitor </div>", unsafe_allow_html=True)
            if st.button("🔄 REFRESH", key="btn_refresh_acq"): st.cache_data.clear(); st.rerun()
            table_rows = "".join([f"""<tr style="border-bottom: 1px solid #2b3a4f;"><td style="padding:14px;"><img src="{c.get('image', '')}" width="22"> <b>{c.get('name')}</b></td><td style="padding:14px;">${c.get('current_price', 0):,}</td><td style="padding:14px;">{c.get('price_change_percentage_24h', 0):.2f}%</td><td style="padding:14px;"><span style="background:{get_risk_info(c.get('price_change_percentage_24h', 0))[1]}; color:#0d1b2a; padding:3px 10px; border-radius:4px; font-weight:900;">{get_risk_info(c.get('price_change_percentage_24h', 0))[0]}</span></td><td style="padding:14px; text-align:right; color:#4cc9f0;">LIVE</td></tr>""" for c in data[:10]])
            full_table_html = f"""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; color:white;"><div style="max-height: 400px; overflow-y: auto;"><table style="width:100%; border-collapse:collapse; text-align:left;"><thead style="position: sticky; top: 0; background: #4cc9f0; z-index: 10;"><tr style="color:white;"><th>CRYPTO</th><th>PRICE (USD)</th><th>24H CHANGE</th><th>RISK STATUS</th><th style="text-align:right;">STATUS</th></tr></thead><tbody>{table_rows}</tbody></table></div></div>"""
            components.html(full_table_html, height=450)

    with tab_about:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>🚀 About</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">Crypto operating on decentralized blockchains.</p>', unsafe_allow_html=True)

    with tab_data_proc:
        dp.render_data_processing(data)

    with tab_reports:
        st.markdown("<h2 style='color:#4cc9f0;'>📑 Export</h2>", unsafe_allow_html=True)
        st.button("📥 DOWNLOAD MARKET SUMMARY (PDF)")

    with tab_viz_dash:
        vz.render_viz_dashboard(data, high_risk, total_coins)

    with tab_risk_class:
        st.markdown("<h1 class='cyan-title'>🛡️ Risk Classification</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.error(f"🔴 **HIGH RISK:** {high_risk} assets")
        c3.success(f"🟢 **LOW RISK:** {low_risk} assets")

    with tab_contact:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>📞 Contact</h2>", unsafe_allow_html=True)
        cont_col1, cont_col2, cont_col3 = st.columns(3)
        with cont_col1: st.markdown("""<div class="insight-box" style="height:200px; text-align:center;">📧 support@cryptorisk.com</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
