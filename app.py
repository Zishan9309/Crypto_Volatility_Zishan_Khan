import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📈",
    layout="wide"
)

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
    if abs_change > 5: return "High", "#ef476f"
    if abs_change > 2: return "Medium", "#ffd166"
    return "Low", "#06d6a0"

# ---------------- MAIN APP ----------------
data = fetch_real_data()

if not data:
    st.error("API Limit reached. Please wait 1 minute.")
    st.stop()

# Header with Refresh Button
head_col1, head_col2 = st.columns([5, 1])
with head_col1:
    st.markdown("<h1 style='color:#4cc9f0;'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
with head_col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

st.write("---")

left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("<h3 style='color:#1b4965;'>📋 Market Risk Monitor</h3>", unsafe_allow_html=True)
    
    # Building the Table HTML
    table_rows = ""
    for coin in data:
        change = coin.get('price_change_percentage_24h', 0) or 0
        risk_text, risk_color = get_risk_info(change)
        change_color = "#06d6a0" if change >= 0 else "#ef476f"
        
        table_rows += f"""
        <tr style="border-bottom: 1px solid #2b3a4f;">
            <td style="padding:15px;"><img src="{coin['image']}" width="20" style="vertical-align:middle;margin-right:10px;"><b>{coin['name']}</b></td>
            <td style="padding:15px;"><b>${coin['current_price']:,}</b></td>
            <td style="padding:15px;color:{change_color};font-weight:bold;">{change:.2f}%</td>
            <td style="padding:15px;"><span style="background:{risk_color};color:#0d1b2a;padding:4px 8px;border-radius:4px;font-weight:bold;font-size:11px;">{risk_text.upper()}</span></td>
        </tr>
        """

    full_html = f"""
    <div style="background:#1b263b; padding:20px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif; color:white;">
        <table style="width:100%; border-collapse:collapse; text-align:left;">
            <thead>
                <tr style="border-bottom: 2px solid #415a77; color:#778da9; font-size:12px;">
                    <th style="padding:10px;">ASSET</th>
                    <th style="padding:10px;">PRICE (USD)</th>
                    <th style="padding:10px;">24H CHANGE</th>
                    <th style="padding:10px;">RISK LEVEL</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """
    # GUARANTEED RENDER: Using components.html
    components.html(full_html, height=600, scrolling=False)

with right_col:
    st.markdown("<h3 style='color:#1b4965;'>📊 7-Day Asset Trend</h3>", unsafe_allow_html=True)
    
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
            paper_bgcolor='#1b263b',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            margin=dict(l=40, r=10, t=10, b=40),
            height=300,
            xaxis=dict(title="Last 7 Days (Hours)", showgrid=False),
            yaxis=dict(title="Price ($)", showgrid=True, gridcolor='#2b3a4f')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# Footer/Status
st.caption(f"Sync: {datetime.now().strftime('%H:%M:%S')} | Data Source: CoinGecko")
