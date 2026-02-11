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

# ---------------- CUSTOM CSS (REFINED FOR TABLE MATCH) ----------------
st.markdown(f"""
<style>
    /* Heading Colors */
    .dark-blue-title {{
        color: #1b4965 !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif;
    }}
    .cyan-title {{
        color: #4cc9f0 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{ background-color: #0d1b2a; color: #e0e1dd; }}
    
    /* Card/Container Styling */
    .custom-card {{
        background-color: #1b263b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #415a77;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }}

    /* REFINED TABLE STYLING TO MATCH IMAGE */
    .crypto-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 8px; /* Spacing between rows for that 'list' look */
        color: #ffffff;
    }}
    .crypto-table th {{
        color: #778da9;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 1px;
        padding: 12px;
        border-bottom: 1px solid #415a77;
        text-align: left;
    }}
    .crypto-table tr {{
        background-color: transparent;
        transition: 0.3s;
    }}
    .crypto-table td {{
        padding: 16px 12px;
        border-bottom: 1px solid #0d1b2a; /* Sublte row separation */
        font-size: 14px;
    }}
    .coin-cell {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
    }}
    .refresh-btn-ui {{
        background-color: transparent;
        border: 1px solid #4cc9f0;
        color: #4cc9f0;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 12px;
        float: right;
    }}

    /* Badges */
    .badge-high {{ background-color: #ef476f; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px; }}
    .badge-med {{ background-color: #ffd166; color: #0d1b2a; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px; }}
    .badge-low {{ background-color: #06d6a0; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px; }}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA FETCHING ----------------
@st.cache_data(ttl=60)
def fetch_real_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
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

# Top Sentiment Row
st.markdown("<h3 class='cyan-title'>🌐 Market Sentiment Heatmap</h3>", unsafe_allow_html=True)
heatmap_data = pd.DataFrame([{
    "Asset": c['symbol'].upper(),
    "Change": c['price_change_percentage_24h'],
    "Size": 1 
} for c in data[:12]])

fig_heat = px.treemap(heatmap_data, path=['Asset'], values='Size',
                      color='Change', color_continuous_scale='RdYlGn',
                      range_color=[-7, 7])
fig_heat.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=140, paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_heat, use_container_width=True)

st.write("---")

left_col, right_col = st.columns([1.6, 1])

with left_col:
    # Heading in Dark Blue
    st.markdown("<h3 class='dark-blue-title'>📋 Market Risk Monitor</h3>", unsafe_allow_html=True)
    
    # Table Container
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Refresh logic inside the card UI
    c_sub1, c_sub2 = st.columns([2, 1])
    with c_sub2:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

    # The HTML Table
    table_html = """
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
    """
    
    for coin in data[:10]:
        change = coin.get('price_change_percentage_24h', 0) or 0
        risk_text, risk_class = get_risk_info(change)
        color = "#06d6a0" if change >= 0 else "#ef476f"
        
        table_html += f"""
        <tr>
            <td>
                <div class="coin-cell">
                    <img src="{coin['image']}" width="24" height="24">
                    <span>{coin['name']} <small style="color:#778da9">({coin['symbol'].upper()})</small></span>
                </div>
            </td>
            <td style="font-weight:700">${coin['current_price']:,}</td>
            <td style="color:{color}; font-weight:600;">{'+' if change > 0 else ''}{change:.2f}%</td>
            <td><span class="{risk_class}">{risk_text.upper()}</span></td>
        </tr>"""
    
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

with right_col:
    # Heading in Dark Blue
    st.markdown("<h3 class='dark-blue-title'>📊 7-Day Asset Trend</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    selected_coin_name = st.selectbox("Detailed Analysis", [c['name'] for c in data[:10]])
    coin = next(c for c in data if c['name'] == selected_coin_name)
    
    if 'sparkline_in_7d' in coin:
        spark_prices = coin['sparkline_in_7d']['price']
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
            margin=dict(l=50, r=20, t=20, b=50),
            height=300,
            xaxis=dict(title="Timeline (Hours)", showgrid=False, showline=True, linecolor='#415a77'),
            yaxis=dict(title="Price ($)", showgrid=True, gridcolor='#2b3a4f', showline=True, linecolor='#415a77')
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Market Movers
st.write("---")
st.markdown("<h3 class='cyan-title'>🔥 Market Movers (24h)</h3>", unsafe_allow_html=True)
sorted_data = sorted(data, key=lambda x: x.get('price_change_percentage_24h', 0) or 0, reverse=True)
top_g = sorted_data[0]
top_l = sorted_data[-1]

movers_col1, movers_col2 = st.columns(2)
with movers_col1:
    st.markdown(f"<div class='custom-card' style='border-left: 4px solid #06d6a0;'><b>TOP GAINER:</b> {top_g['name']} <span style='color:#06d6a0'>+{top_g['price_change_percentage_24h']:.2f}%</span></div>", unsafe_allow_html=True)
with movers_col2:
    st.markdown(f"<div class='custom-card' style='border-left: 4px solid #ef476f;'><b>TOP LOSER:</b> {top_l['name']} <span style='color:#ef476f'>{top_l['price_change_percentage_24h']:.2f}%</span></div>", unsafe_allow_html=True)

st.caption(f"Live Data Stream: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
