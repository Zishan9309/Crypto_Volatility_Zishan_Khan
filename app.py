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
    /* Dark Blue Color for Titles and Sections */
    .dark-blue-title {
        color: #1b4965 !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif;
        margin-bottom: 10px;
    }
    
    .stApp { background-color: #0d1b2a; color: #e0e1dd; }
    
    /* Card Styling */
    .metric-card {
        background-color: #1b263b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #415a77;
        text-align: center;
    }
    
    /* Table Styling */
    .crypto-table { width: 100%; border-collapse: collapse; color: white; }
    .crypto-table th { color: #778da9; text-align: left; padding: 12px; border-bottom: 2px solid #415a77; }
    .crypto-table td { padding: 15px; border-bottom: 1px solid #1b263b; }
    
    .badge-high { background-color: #ef476f; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-med { background-color: #ffd166; color: #0d1b2a; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-low { background-color: #06d6a0; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
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

# Heading in Dark Blue
st.markdown("<h1 class='dark-blue-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)

# Aesthetic Sentiment Row (New Feature)
st.markdown("### 🌐 Market Heatmap (Sentiment)")
heatmap_data = pd.DataFrame([{
    "Asset": c['symbol'].upper(),
    "Change": c['price_change_percentage_24h'],
    "Size": 1 # Uniform size for aesthetic look
} for c in data])

fig_heat = px.treemap(heatmap_data, path=['Asset'], values='Size',
                      color='Change', color_continuous_scale='RdYlGn',
                      range_color=[-10, 10])
fig_heat.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=150, paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_heat, use_container_width=True)

st.write("---")

left_col, right_col = st.columns([1.5, 1])

with left_col:
    # Changed "Market Risk Monitor" to Dark Blue
    st.markdown("<h3 class='dark-blue-title'>📋 Market Risk Monitor</h3>", unsafe_allow_html=True)
    
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
    st.markdown("<h3 class='dark-blue-title'>📊 7-Day Asset Trend</h3>", unsafe_allow_html=True)
    selected_coin_name = st.selectbox("Select Asset", [c['name'] for c in data])
    coin = next(c for c in data if c['name'] == selected_coin_name)
    
    # 7-DAY CHART WITH AXES AND VALUES
    if 'sparkline_in_7d' in coin:
        spark_prices = coin['sparkline_in_7d']['price']
        # Creating x-axis labels (hours)
        hours = list(range(len(spark_prices)))
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=hours, y=spark_prices,
            mode='lines',
            line=dict(color='#4cc9f0', width=3),
            fill='tozeroy',
            fillcolor='rgba(76, 201, 240, 0.1)'
        ))
        
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            margin=dict(l=40, r=20, t=20, b=40),
            height=300,
            xaxis=dict(
                title="Hours (Last 7 Days)",
                showgrid=False,
                showline=True,
                linecolor='#415a77'
            ),
            yaxis=dict(
                title="Price (USD)",
                showgrid=True,
                gridcolor='#1b263b',
                showline=True,
                linecolor='#415a77'
            )
        )
        st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.caption(f"Sync: {datetime.now().strftime('%H:%M:%S')} | Concept: Risk Matrix v1.2")
