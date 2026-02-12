import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📈",
    layout="wide"
)

# ---------------- INITIALIZE SESSION STATE ----------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ---------------- SHARED CSS (Login & Dashboard) ----------------
st.markdown("""
<style>
    .stApp { background-color: #0d1b2a !important; }
    
    /* Login Card Styling */
    .login-box {
        background-color: #1b263b;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #4cc9f0;
        max-width: 400px;
        margin: auto;
        text-align: center;
        box-shadow: 0 0 20px rgba(76, 201, 240, 0.2);
    }
    
    .cyan-title {
        color: #4cc9f0 !important;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .dark-blue-section {
        color: #1b4965 !important;
        font-weight: 800;
        font-size: 26px;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #4cc9f0;
        color: #0d1b2a;
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE FUNCTION ----------------
def login_page():
    st.write("#") # Spacer
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h2 class='cyan-title'>System Login</h2>", unsafe_allow_html=True)
        st.write("Enter credentials to access Risk Monitor")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("AUTHENTICATE"):
            # You can change these credentials
            if username == "admin" and password == "crypto123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE FUNCTION ----------------
def dashboard_page():
    # --- DATA FETCHING ---
    @st.cache_data(ttl=60)
    def fetch_real_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 20, "page": 1, "sparkline": "true", "price_change_percentage": "24h"}
        try:
            r = requests.get(url, params=params)
            return r.json()
        except: return []

    data = fetch_real_data()
    if not data:
        st.error("API Limit reached. Wait 1 min.")
        st.stop()

    # --- TOP BAR ---
    head_left, head_right = st.columns([5, 1])
    with head_left:
        st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
    with head_right:
        if st.sidebar.button("LOGOUT"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- MAIN TABLE ---
    st.markdown("<div class='dark-blue-section'>📋 Market Risk Monitor</div>", unsafe_allow_html=True)
    
    def get_risk_info(change):
        abs_c = abs(change or 0)
        if abs_c > 5: return "HIGH", "#ef476f"
        if abs_c > 2: return "MEDIUM", "#ffd166"
        return "LOW", "#06d6a0"

    table_rows = ""
    for coin in data:
        risk_text, risk_color = get_risk_info(coin.get('price_change_percentage_24h', 0))
        table_rows += f"""
        <tr style="border-bottom: 1px solid #2b3a4f; color:white;">
            <td style="padding:12px;"><img src="{coin['image']}" width="20"> {coin['name']}</td>
            <td style="padding:12px;">${coin['current_price']:,}</td>
            <td style="padding:12px;">{coin.get('price_change_percentage_24h', 0):.2f}%</td>
            <td style="padding:12px;"><span style="background:{risk_color}; color:#0d1b2a; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:10px;">{risk_text}</span></td>
        </tr>"""

    full_table_html = f"""
    <div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif;">
        <div style="max-height: 350px; overflow-y: auto;">
            <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead style="position: sticky; top: 0; background: #1b263b; color:#778da9; font-size:11px;">
                    <tr><th style="padding:10px;">ASSET</th><th style="padding:10px;">PRICE</th><th style="padding:10px;">24H CHANGE</th><th style="padding:10px;">RISK</th></tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
    </div>"""
    components.html(full_table_html, height=400)

    # --- CHARTS SECTION ---
    st.write("---")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown("<div class='dark-blue-section'>📊 7-Day Asset Trend</div>", unsafe_allow_html=True)
        sel = st.selectbox("Select Asset", [c['name'] for c in data])
        coin_obj = next(c for c in data if c['name'] == sel)
        fig = go.Figure(go.Scatter(y=coin_obj['sparkline_in_7d']['price'], line=dict(color='#4cc9f0', width=3), fill='tozeroy', fillcolor='rgba(76, 201, 240, 0.1)'))
        fig.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300, margin=dict(l=40,r=10,t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("<h3 class='cyan-title' style='font-size:15px;'>🛡️ Risk Distribution</h3>", unsafe_allow_html=True)
        risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for c in data:
            r_txt, _ = get_risk_info(c['price_change_percentage_24h'])
            risk_counts[r_txt] += 1
        fig_p = px.pie(values=list(risk_counts.values()), names=list(risk_counts.keys()), color_discrete_sequence=['#06d6a0','#ffd166','#ef476f'])
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
        st.plotly_chart(fig_p, use_container_width=True)

# ---------------- MAIN LOGIC ----------------
if st.session_state['logged_in']:
    dashboard_page()
else:
    login_page()
