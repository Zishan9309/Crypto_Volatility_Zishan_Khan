import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Volatility & Risk Analyzer", layout="wide")

# --- CUSTOM CSS FOR EXACT UI MATCH ---
# FIXED: Changed unsafe_allow_index to unsafe_allow_html
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    
    h1, h2, h3 {
        color: #4cc9f0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Card Container */
    .card {
        background-color: #1b263b;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #415a77;
        margin-bottom: 20px;
    }
    
    /* Custom Table Styling */
    .crypto-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .crypto-table th {
        text-align: left;
        color: #778da9;
        padding-bottom: 12px;
        border-bottom: 1px solid #415a77;
        font-size: 0.9rem;
    }
    .crypto-table td {
        padding: 18px 0;
        border-bottom: 1px solid #0d1b2a;
    }
    .price-text { color: #ffffff; font-weight: bold; }
    .change-pos { color: #06d6a0; }
    .change-neg { color: #ef476f; }
    
    /* Risk Badges */
    .risk-high { color: #ef476f; font-weight: bold; border: 1px solid #ef476f; padding: 2px 8px; border-radius: 5px; }
    .risk-med { color: #ffd166; font-weight: bold; border: 1px solid #ffd166; padding: 2px 8px; border-radius: 5px; }
    .risk-low { color: #06d6a0; font-weight: bold; border: 1px solid #06d6a0; padding: 2px 8px; border-radius: 5px; }

    /* Button Styling */
    .stButton>button {
        background-color: transparent;
        color: #4cc9f0;
        border: 1px solid #4cc9f0;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4cc9f0;
        color: #0d1b2a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- RISK CALCULATION ENGINE ---
def calculate_volatility(sparkline_data):
    if not sparkline_data:
        return 0, "N/A", "risk-low"
    
    prices = np.array(sparkline_data)
    returns = np.diff(prices) / prices[:-1]
    
    volatility = np.std(returns) * 100 
    
    if volatility > 1.5:
        risk_level = "High"
        color_class = "risk-high"
    elif volatility > 0.8:
        risk_level = "Medium"
        color_class = "risk-med"
    else:
        risk_level = "Low"
        color_class = "risk-low"
        
    return volatility, risk_level, color_class

# --- DATA FETCHING ---
@st.cache_data(ttl=60)
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,cardano,polkadot",
        "order": "market_cap_desc",
        "sparkline": "true",
        "price_change_percentage": "24h"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

# --- DASHBOARD HEADER ---
st.title("Crypto Volatility & Risk Analyzer")

col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.markdown("""
    <div class="card">
        <h3>📋 Project Overview</h3>
        <p>This analyzer tracks real-time market data and calculates the <b>Standard Deviation</b> of price movements to determine asset risk.</p>
        <hr style="border-color: #415a77">
        <p><b>Current Phase:</b> Milestone 1 - Live Dashboard</p>
        <p><b>Data Provider:</b> CoinGecko API</p>
        <p><b>Risk Model:</b> 7-Day Variance Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    data = fetch_crypto_data()
    if data:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Trend Visualizer")
        selected_coin_name = st.selectbox("Choose Asset", [c['name'] for c in data])
        coin = next(item for item in data if item["name"] == selected_coin_name)
        
        vol, risk_label, risk_class = calculate_volatility(coin['sparkline_in_7d']['price'])
        
        st.metric("Volatility Index", f"{vol:.2f}%")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=coin['sparkline_in_7d']['price'],
            line=dict(color='#4cc9f0', width=2),
            fill='tozeroy',
            fillcolor='rgba(76, 201, 240, 0.05)'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=180, margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    header_col1, header_col2 = st.columns([2, 1])
    with header_col1:
        st.subheader("☁️ Live Risk Monitor")
    with header_col2:
        if st.button("Refresh API Data"):
            st.cache_data.clear()
            st.rerun()

    if not data:
        st.error("Failed to fetch data. Please wait or check API limit.")
    else:
        table_html = """
        <table class="crypto-table">
            <tr>
                <th>ASSET</th>
                <th>PRICE (USD)</th>
                <th>24H CHANGE</th>
                <th>RISK LEVEL</th>
            </tr>
        """
        
        for coin in data:
            change = coin['price_change_percentage_24h']
            change_color = "change-pos" if change >= 0 else "change-neg"
            _, risk_text, risk_css = calculate_volatility(coin['sparkline_in_7d']['price'])
            
            table_html += f"""
            <tr>
                <td><span style="color:#4cc9f0">●</span> {coin['name']}</td>
                <td class="price-text">${coin['current_price']:,}</td>
                <td class="{change_color}">{'+' if change > 0 else ''}{change:.2f}%</td>
                <td><span class="{risk_css}">{risk_text.upper()}</span></td>
            </tr>
            """
        
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)
