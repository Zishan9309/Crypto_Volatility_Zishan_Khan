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
    page_icon="📈",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Heading Colors */
    .dark-blue-title {
        color: #1b4965 !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif;
        margin-bottom: 15px;
        display: block;
    }
    .cyan-title {
        color: #4cc9f0 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
        margin-bottom: 10px;
    }
    
    .stApp { background-color: #0d1b2a; color: #e0e1dd; }
    
    /* Card/Container Styling */
    .custom-card {
        background-color: #1b263b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #415a77;
        margin-bottom: 20px;
    }

    /* TABLE STYLING */
    .crypto-table {
        width: 100%;
        border-collapse: collapse;
        color: #ffffff;
    }
    .crypto-table th {
        color: #778da9;
        text-transform: uppercase;
        font-size: 12px;
        padding: 12px;
        border-bottom: 2px solid #415a77;
        text-align: left;
    }
    .crypto-table td {
        padding: 15px 12px;
        border-bottom: 1px solid #2b3a4f;
        font-size: 14px;
    }
    .badge-high { background-color: #ef476f; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-med { background-color: #ffd166; color: #0d1b2a; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-low { background-color: #06d6a0; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
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
    st.error("API Limit reached. Please wait 1 minute.")
    st.stop()

# Header Section
st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)

st.write("---")

left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("<span class='dark-blue-title'>📋 Market Risk Monitor</span>", unsafe_allow_html=True)
    
    # Building the table as a single clean string
    table_rows = ""
    for coin in data:
        change = coin.get('price_change_percentage_24h', 0) or 0
        risk_text, risk_class = get_risk_info(change)
        color = "#06d6a0" if change >= 0 else "#ef476f"
        
        row = f"""
        <tr>
            <td><img src="{coin['image']}" width="20" style="margin-right:10px;"><b>{coin['name']}</b></td>
            <td><b>${coin['current_price']:,}</b></td>
            <td style="color:{color}; font-weight:bold;">{change:.2f}%</td>
            <td><span class="{risk_class}">{risk_text.upper()}</span></td>
        </tr>
        """
        table_rows += row

    full_table_html = f"""
    <div class="custom-card">
        <table class="crypto-table">
            <thead>
                <tr>
                    <th>Asset</th>
                    <th>Price (USD)</th>
                    <th>24h Change</th>
                    <th>Risk Level</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """
    
    # THE KEY FIX: Using st.components.v1.html or ensuring st.markdown handles it
    st.markdown(full_table_html, unsafe_allow_html=True)

with right_col:
    st.markdown("<span class='dark-blue-title'>📊 7-Day Asset Trend</span>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    selected_coin_name = st.selectbox("Select Coin", [c['name'] for c in data])
    coin = next(c for c in data if c['name'] == selected_coin_name)
    
    if 'sparkline_in_7d' in coin:
        spark_prices = coin['sparkline_in_7d']['price']
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            y=spark_prices,
            mode='lines',
            line=dict(color='#4cc9f0', width=3),
            fill='tozeroy',
            fillcolor='rgba(76, 201, 240, 0.1)'
        ))
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            margin=dict(l=40, r=10, t=10, b=40),
            height=300,
            xaxis=dict(title="Last 7 Days (Hours)", showgrid=False),
            yaxis=dict(title="Price ($)", showgrid=True, gridcolor='#2b3a4f')
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Aesthetic Market Sentiment Heatmap
st.write("---")
st.markdown("<h3 class='cyan-title'>🌐 Market Sentiment Heatmap</h3>", unsafe_allow_html=True)
heatmap_data = pd.DataFrame([{"Asset": c['symbol'].upper(), "Change": c['price_change_percentage_24h'], "Size": 1} for c in data])
fig_heat = px.treemap(heatmap_data, path=['Asset'], values='Size', color='Change', color_continuous_scale='RdYlGn', range_color=[-7, 7])
fig_heat.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=140, paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_heat, use_container_width=True)

st.caption(f"Sync: {datetime.now().strftime('%H:%M:%S')}")
