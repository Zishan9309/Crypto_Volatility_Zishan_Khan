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

# ---------------- CUSTOM CSS (EXACT MATCH TO YOUR IMAGE) ----------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    
    /* Card Styling */
    .metric-card {
        background-color: #1b263b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #415a77;
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #4cc9f0;
    }
    
    /* Table Headers */
    .crypto-table {
        width: 100%;
        border-collapse: collapse;
        color: white;
    }
    .crypto-table th {
        color: #778da9;
        text-align: left;
        padding: 12px;
        border-bottom: 2px solid #415a77;
    }
    .crypto-table td {
        padding: 15px;
        border-bottom: 1px solid #1b263b;
    }

    /* Risk Badges */
    .badge-high { background-color: #ef476f; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-med { background-color: #ffd166; color: #0d1b2a; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-low { background-color: #06d6a0; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }

    /* Custom Title */
    .main-title {
        color: #4cc9f0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
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
        "per_page": 10,
        "page": 1,
        "sparkline": True, # Needed for the trend charts
        "price_change_percentage": "24h"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

# ---------------- RISK LOGIC ----------------
def get_risk_info(change):
    abs_change = abs(change)
    if abs_change > 5: return "High", "badge-high"
    if abs_change > 2: return "Medium", "badge-med"
    return "Low", "badge-low"

# ---------------- MAIN APP ----------------
data = fetch_real_data()

if not data:
    st.error("API Limit reached or Connection Error. Please refresh in 1 minute.")
    st.stop()

# Header Section
st.markdown("<h1 class='main-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.caption(f"Market Status: Live | Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# KPI Row
cols = st.columns(4)
with cols[0]:
    st.markdown(f"<div class='metric-card'><h3>BTC Price</h3><h2 style='color:#4cc9f0'>${data[0]['current_price']:,}</h2></div>", unsafe_allow_html=True)
with cols[1]:
    vol_avg = np.mean([abs(c['price_change_percentage_24h']) for c in data])
    st.markdown(f"<div class='metric-card'><h3>Avg Volatility</h3><h2 style='color:#ffd166'>{vol_avg:.2f}%</h2></div>", unsafe_allow_html=True)
with cols[2]:
    high_risk_count = sum(1 for c in data if abs(c['price_change_percentage_24h']) > 5)
    st.markdown(f"<div class='metric-card'><h3>High Risk Assets</h3><h2 style='color:#ef476f'>{high_risk_count}</h2></div>", unsafe_allow_html=True)
with cols[3]:
    st.markdown("<div class='metric-card'><h3>API Status</h3><h2 style='color:#06d6a0'>Online</h2></div>", unsafe_allow_html=True)

st.write("---")

# Main Content Area
left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.markdown("### 📋 Market Risk Monitor")
    
    # Building the Custom Styled Table
    table_html = """
    <table class="crypto-table">
        <tr>
            <th>Asset</th>
            <th>Price (USD)</th>
            <th>24h Change</th>
            <th>Risk Level</th>
        </tr>
    """
    
    for coin in data:
        change = coin['price_change_percentage_24h'] or 0
        risk_text, risk_class = get_risk_info(change)
        color = "#06d6a0" if change >= 0 else "#ef476f"
        
        table_html += f"""
        <tr>
            <td><img src="{coin['image']}" width="20"> <b>{coin['name']}</b></td>
            <td>${coin['current_price']:,}</td>
            <td style="color:{color}">{change:.2f}%</td>
            <td><span class="{risk_class}">{risk_text}</span></td>
        </tr>
        """
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

with right_col:
    st.markdown("### 📊 Selected Asset Depth")
    selected_coin_name = st.selectbox("Analyze Specific Coin", [c['name'] for c in data])
    coin = next(c for c in data if c['name'] == selected_coin_name)
    
    # 1. Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = abs(coin['price_change_percentage_24h']),
        title = {'text': "24h Volatility Intensity"},
        gauge = {
            'axis': {'range': [0, 10]},
            'bar': {'color': "#4cc9f0"},
            'steps': [
                {'range': [0, 2], 'color': "rgba(6, 214, 160, 0.2)"},
                {'range': [2, 5], 'color': "rgba(255, 209, 102, 0.2)"},
                {'range': [5, 10], 'color': "rgba(239, 71, 111, 0.2)"}
            ]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=250, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # 2. Sparkline (7-Day Trend)
    st.markdown(f"**7-Day {selected_coin_name} Trend**")
    spark_data = coin['sparkline_in_7d']['price']
    fig_spark = px.line(spark_data, color_discrete_sequence=['#4cc9f0'])
    fig_spark.update_layout(
        xaxis_visible=False, yaxis_visible=False, 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0), height=100
    )
    st.plotly_chart(fig_spark, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Developed for Crypto Volatility & Risk Analysis | Milestone 1 Complete")
