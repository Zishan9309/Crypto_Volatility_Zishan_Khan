import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📉",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp { background-color: #0d1b2a; color: #e0e1dd; }
    .metric-card {
        background-color: #1b263b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #415a77;
        text-align: center;
    }
    .crypto-table { width: 100%; border-collapse: collapse; color: white; }
    .crypto-table th { color: #778da9; text-align: left; padding: 12px; border-bottom: 2px solid #415a77; }
    .crypto-table td { padding: 15px; border-bottom: 1px solid #1b263b; }
    .badge-high { background-color: #ef476f; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-med { background-color: #ffd166; color: #0d1b2a; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-low { background-color: #06d6a0; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .main-title { color: #4cc9f0; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA FETCHING ----------------
@st.cache_data(ttl=60)
def fetch_real_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
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
    if abs_change > 5: return "High", "badge-high"
    if abs_change > 2: return "Medium", "badge-med"
    return "Low", "badge-low"

# ---------------- MAIN APP ----------------
data = fetch_real_data()

if not data:
    st.error("API Limit reached. Please wait 1 minute and refresh.")
    st.stop()

st.markdown("<h1 class='main-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)

# KPI Row
cols = st.columns(4)
with cols[0]:
    st.markdown(f"<div class='metric-card'><h3>BTC Price</h3><h2 style='color:#4cc9f0'>${data[0]['current_price']:,}</h2></div>", unsafe_allow_html=True)
with cols[1]:
    vol_avg = np.mean([abs(c.get('price_change_percentage_24h', 0) or 0) for c in data])
    st.markdown(f"<div class='metric-card'><h3>Avg Volatility</h3><h2 style='color:#ffd166'>{vol_avg:.2f}%</h2></div>", unsafe_allow_html=True)
with cols[2]:
    high_risk_count = sum(1 for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5)
    st.markdown(f"<div class='metric-card'><h3>High Risk Assets</h3><h2 style='color:#ef476f'>{high_risk_count}</h2></div>", unsafe_allow_html=True)
with cols[3]:
    st.markdown("<div class='metric-card'><h3>Market Status</h3><h2 style='color:#06d6a0'>Active</h2></div>", unsafe_allow_html=True)

st.write("---")

left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.markdown("### 📋 Market Risk Monitor")
    
    table_html = """<table class="crypto-table"><tr><th>Asset</th><th>Price (USD)</th><th>24h Change</th><th>Risk Level</th></tr>"""
    
    for coin in data:
        change = coin.get('price_change_percentage_24h', 0) or 0
        risk_text, risk_class = get_risk_info(change)
        color = "#06d6a0" if change >= 0 else "#ef476f"
        
        table_html += f"""
        <tr>
            <td><img src="{coin['image']}" width="20"> {coin['name']}</td>
            <td>${coin['current_price']:,}</td>
            <td style="color:{color}">{change:.2f}%</td>
            <td><span class="{risk_class}">{risk_text}</span></td>
        </tr>"""
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

with right_col:
    st.markdown("### 📊 Asset Depth Analysis")
    selected_coin_name = st.selectbox("Analyze Specific Coin", [c['name'] for c in data])
    coin = next(c for c in data if c['name'] == selected_coin_name)
    
    # GAUGE CHART
    change_val = abs(coin.get('price_change_percentage_24h', 0) or 0)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = change_val,
        title = {'text': "Volatility Intensity"},
        gauge = {
            'axis': {'range': [0, 10]},
            'bar': {'color': "#4cc9f0"},
            'steps': [
                {'range': [0, 2], 'color': "#06d6a0"},
                {'range': [2, 5], 'color': "#ffd166"},
                {'range': [5, 10], 'color': "#ef476f"}
            ]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=250, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # FIXED SPARKLINE LOGIC
    st.markdown(f"**7-Day {selected_coin_name} Price Action**")
    
    # Safety Check for 'sparkline_in_7d'
    if 'sparkline_in_7d' in coin and 'price' in coin['sparkline_in_7d']:
        spark_data = coin['sparkline_in_7d']['price']
        fig_spark = px.line(spark_data, color_discrete_sequence=['#4cc9f0'])
        fig_spark.update_layout(
            xaxis_visible=False, yaxis_visible=False, 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=0,b=0), height=120
        )
        st.plotly_chart(fig_spark, use_container_width=True)
    else:
        st.warning("Sparkline data unavailable for this asset.")

st.markdown("---")
st.caption(f"Data via CoinGecko | Sync Time: {datetime.now().strftime('%H:%M:%S')}")
