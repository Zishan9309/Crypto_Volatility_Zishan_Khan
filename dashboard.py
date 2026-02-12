import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def main():
    # ---------------- UI STYLING ----------------
    st.markdown("""
    <style>
        .stApp { background-color: #0d1b2a !important; }
        header, [data-testid="stHeader"] { background-color: #0d1b2a !important; }
        
        .cyan-title {
            color: #4cc9f0 !important;
            font-weight: 800;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }
        
        .stPlotlyChart {
            background-color: #1b263b;
            border-radius: 12px;
            border: 1px solid #415a77;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- DATA FETCHING WITH SAFETY ----------------
    @st.cache_data(ttl=60)
    def fetch_real_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 25,
            "page": 1,
            "sparkline": "true",
            "price_change_percentage": "24h"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return [] # Return empty list if API limit hit
        except Exception:
            return []

    def get_risk_info(change):
        abs_change = abs(change or 0)
        if abs_change > 5: return "HIGH", "#ef476f"
        if abs_change > 2: return "MEDIUM", "#ffd166"
        return "LOW", "#06d6a0"

    # ---------------- MAIN APP LOGIC ----------------
    data = fetch_real_data()

    # 1. MAIN HEADING
    head_left, head_right = st.columns([4, 1])
    with head_left:
        st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
    with head_right:
        if st.button("🔄 REFRESH SYSTEM"):
            st.cache_data.clear()
            st.rerun()

    st.write("---")

    # ERROR HANDLING UI
    if not data or not isinstance(data, list):
        st.warning("⚠️ API connection busy or limit reached. Please wait a moment and click Refresh.")
        st.stop()

    # 2. SCROLLABLE MARKET RISK MONITOR
    st.markdown("<div class='cyan-title'>📋 Market Risk Monitor </div>", unsafe_allow_html=True)

    table_rows = ""
    for coin in data:
        # Extra safety check: ensure coin is a dictionary
        if isinstance(coin, dict):
            change = coin.get('price_change_percentage_24h', 0) or 0
            risk_text, risk_color = get_risk_info(change)
            change_color = "#06d6a0" if change >= 0 else "#ef476f"
            
            table_rows += f"""
            <tr style="border-bottom: 1px solid #2b3a4f;">
                <td style="padding:14px;"><img src="{coin.get('image', '')}" width="22" style="vertical-align:middle;margin-right:12px;"><b>{coin.get('name', 'Unknown')}</b></td>
                <td style="padding:14px; font-family:monospace;">${coin.get('current_price', 0):,}</td>
                <td style="padding:14px; color:{change_color}; font-weight:bold;">{change:.2f}%</td>
                <td style="padding:14px;"><span style="background:{risk_color}; color:#0d1b2a; padding:3px 10px; border-radius:4px; font-weight:900; font-size:10px;">{risk_text}</span></td>
            </tr>
            """

    full_table_html = f"""
    <div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif; color:white;">
        <div style="max-height: 400px; overflow-y: auto; scrollbar-width: thin; scrollbar-color: #4cc9f0 #1b263b;">
            <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead style="position: sticky; top: 0; background: #1b263b; z-index: 10;">
                    <tr style="border-bottom: 2px solid #415a77; color:#778da9; font-size:11px; letter-spacing:1px;">
                        <th style="padding:12px;">ASSET</th>
                        <th style="padding:12px;">PRICE (USD)</th>
                        <th style="padding:12px;">24H CHANGE</th>
                        <th style="padding:12px;">RISK STATUS</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
    </div>
    """
    components.html(full_table_html, height=450)

    st.write("---")

    # 3. CHARTS SECTION
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.markdown("<div class='cyan-title'>📊 7-Day Asset Trend</div>", unsafe_allow_html=True)
        coin_names = [c.get('name') for c in data if isinstance(c, dict)]
        selected_coin = st.selectbox("SELECT COIN FOR DEPTH ANALYSIS", coin_names)
        
        coin_obj = next((c for c in data if c.get('name') == selected_coin), None)
        
        if coin_obj and 'sparkline_in_7d' in coin_obj:
            y_data = coin_obj['sparkline_in_7d']['price']
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(y=y_data, mode='lines', line=dict(color='#4cc9f0', width=3), fill='tozeroy', fillcolor='rgba(76, 201, 240, 0.1)'))
            fig_t.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300, margin=dict(l=40,r=10,t=10,b=40))
            st.plotly_chart(fig_t, use_container_width=True)

    with col_b:
        st.markdown("<h3 class='cyan-title' style='font-size:15px;'>🛡️ Risk Distribution</h3>", unsafe_allow_html=True)
        risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for c in data:
            if isinstance(c, dict):
                r_txt, _ = get_risk_info(c.get('price_change_percentage_24h', 0))
                risk_counts[r_txt] += 1
        
        fig_p = px.pie(values=list(risk_counts.values()), names=list(risk_counts.keys()), 
                        color=list(risk_counts.keys()), color_discrete_map={'LOW':'#06d6a0','MEDIUM':'#ffd166','HIGH':'#ef476f'})
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig_p, use_container_width=True)

    st.caption(f"SYSTEM LIVE | SYNC: {datetime.now().strftime('%H:%M:%S')} | NAGPUR, MH")

if __name__ == "__main__":
    main()
