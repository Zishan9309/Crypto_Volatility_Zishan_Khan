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

# ---------------- EXACT BODY & UI STYLING ----------------
st.markdown("""
<style>
    /* Force exact background color from image */
    .stApp {
        background-color: #0d1b2a !important;
    }
    header, [data-testid="stHeader"] {
        background-color: #0d1b2a !important;
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
        font-size: 24px;
        margin-bottom: 10px;
    }

    /* Standard Card for Plotly Charts */
    .stPlotlyChart {
        background-color: #1b263b;
        border-radius: 12px;
        border: 1px solid #415a77;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA FETCHING ----------------
@st.cache_data(ttl=60)
def fetch_real_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 12,
        "page": 1,
        "sparkline": "true",
        "price_change_percentage": "24h"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

def get_risk_info(change):
    abs_change = abs(change or 0)
    if abs_change > 5: return "HIGH", "#ef476f"
    if abs_change > 2: return "MEDIUM", "#ffd166"
    return "LOW", "#06d6a0"

# ---------------- MAIN APP ----------------
data = fetch_real_data()

if not data:
    st.error("API Limit reached. Please wait 1 minute.")
    st.stop()

# Header Section
head_left, head_right = st.columns([4, 1])
with head_left:
    st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
with head_right:
    if st.button("🔄 REFRESH SYSTEM"):
        st.cache_data.clear()
        st.rerun()

st.write("---")

# Row 1: Market Overview Charts
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<h3 class='cyan-title' style='font-size:15px;'>🌐 Market Volatility Heatmap</h3>", unsafe_allow_html=True)
    h_df = pd.DataFrame([{"Asset": c['symbol'].upper(), "Vol": c['price_change_percentage_24h']} for c in data])
    fig_h = px.bar(h_df, x='Asset', y='Vol', color='Vol', color_continuous_scale='RdYlGn')
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250, margin=dict(t=10,b=10))
    st.plotly_chart(fig_h, use_container_width=True)

with col_b:
    st.markdown("<h3 class='cyan-title' style='font-size:15px;'>🛡️ Risk Distribution</h3>", unsafe_allow_html=True)
    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for c in data:
        r_txt, _ = get_risk_info(c['price_change_percentage_24h'])
        risk_counts[r_txt] += 1
    fig_p = px.pie(values=list(risk_counts.values()), names=list(risk_counts.keys()), 
                   color=list(risk_counts.keys()), color_discrete_map={'LOW':'#06d6a0','MEDIUM':'#ffd166','HIGH':'#ef476f'})
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=250, margin=dict(t=10,b=10))
    st.plotly_chart(fig_p, use_container_width=True)

# Row 2: The Main Monitor & Trend
left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("<div class='cyan-title'>📋 Market Risk Monitor</div>", unsafe_allow_html=True)
    
    # Table HTML Construction
    table_rows = ""
    for coin in data[:10]:
        change = coin.get('price_change_percentage_24h', 0) or 0
        risk_text, risk_color = get_risk_info(change)
        change_color = "#06d6a0" if change >= 0 else "#ef476f"
        
        table_rows += f"""
        <tr style="border-bottom: 1px solid #2b3a4f;">
            <td style="padding:14px;"><img src="{coin['image']}" width="22" style="vertical-align:middle;margin-right:12px;"><b>{coin['name']}</b></td>
            <td style="padding:14px; font-family:monospace;">${coin['current_price']:,}</td>
            <td style="padding:14px; color:{change_color}; font-weight:bold;">{change:.2f}%</td>
            <td style="padding:14px;"><span style="background:{risk_color}; color:#0d1b2a; padding:3px 10px; border-radius:4px; font-weight:900; font-size:10px;">{risk_text}</span></td>
        </tr>
        """

    full_table_html = f"""
    <div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color:white;">
        <table style="width:100%; border-collapse:collapse; text-align:left;">
            <thead>
                <tr style="border-bottom: 2px solid #415a77; color:#778da9; font-size:11px; letter-spacing:1px;">
                    <th style="padding:12px;">ASSET</th>
                    <th style="padding:12px;">PRICE (USD)</th>
                    <th style="padding:12px;">24H CHANGE</th>
                    <th style="padding:12px;">RISK STATUS</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """
    components.html(full_table_html, height=550)

with right_col:
    st.markdown("<div class='cyan-title'>📊 7-Day Asset Trend</div>", unsafe_allow_html=True)
    
    selected_coin = st.selectbox("ANALYZE DEPTH", [c['name'] for c in data])
    coin_obj = next(c for c in data if c['name'] == selected_coin)
    
    if 'sparkline_in_7d' in coin_obj:
        y_data = coin_obj['sparkline_in_7d']['price']
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(y=y_data, mode='lines', line=dict(color='#4cc9f0', width=3), fill='tozeroy', fillcolor='rgba(76, 201, 240, 0.1)'))
        fig_t.update_layout(
            paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white",
            margin=dict(l=40, r=10, t=10, b=40), height=350,
            xaxis=dict(title="Timeline (Hours)", showgrid=False),
            yaxis=dict(title="USD", showgrid=True, gridcolor='#2b3a4f')
        )
        st.plotly_chart(fig_t, use_container_width=True)

st.write("---")
st.caption(f"SYSTEM LIVE | SYNC: {datetime.now().strftime('%H:%M:%S')} | LOCATION: NAGPUR, MH")
