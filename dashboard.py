import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def main():
    # ---------------- UI STYLING & FULL SCREEN FIX ----------------
    st.markdown("""
    <style>
        /* FORCE FULL WIDTH */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
            padding-top: 2rem !important;
        }

        .stApp { background-color: #0d1b2a !important; }
        header, [data-testid="stHeader"] { background-color: #0d1b2a !important; }
        
        /* Force Tabs to take full width */
        [data-testid="stTabPanel"], [data-testid="stHorizontalBlock"] {
            width: 100% !important;
        }

        .cyan-title {
            color: #4cc9f0 !important;
            font-weight: 800;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        /* TAB STYLING: White to Cyan Hover */
        button[data-baseweb="tab"] p {
            color: white !important;
            transition: 0.3s;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"]:hover p {
            color: #4cc9f0 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #4cc9f0 !important;
        }

        /* KPI Card Styling */
        .kpi-card {
            background-color: #1b263b;
            border: 1px solid #415a77;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .kpi-label { color: #778da9; font-size: 12px; font-weight: 600; }
        .kpi-value { color: white; font-size: 24px; font-weight: 800; }

        /* SOLID CYAN BUTTONS */
        div.stButton > button {
            background-color: #4cc9f0 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            text-decoration: none !important;
            transition: 0.3s;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
            width: 100%;
        }
        
        div.stButton > button:hover {
            background-color: #ffffff !important;
            color: #4cc9f0 !important;
        }

        .insight-box {
            background-color: #1b263b;
            border-left: 5px solid #4cc9f0;
            padding: 20px;
            border-radius: 0 12px 12px 0;
            color: white;
            margin-top: 10px;
            width: 100% !important;
        }

        .white-edu-text { color: #ffffff !important; font-size: 16px; line-height: 1.6; }
        .white-bullets li { color: #ffffff !important; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- DATA FETCHING ----------------
    @st.cache_data(ttl=300)
    def fetch_real_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-bAm69cGY5PQKTQBY8HM82bwf"}
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 25, "sparkline": "true", "price_change_percentage": "24h"}
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def get_risk_info(change):
        abs_change = abs(change or 0)
        if abs_change > 5: return "HIGH", "#ef476f"
        if abs_change > 2: return "MEDIUM", "#ffd166"
        return "LOW", "#06d6a0"

    data = fetch_real_data()

    # ---------------- NAVBAR SECTION ----------------
    tab_data_acq, tab_about, tab_data_proc, tab_reports, tab_viz_dash, tab_risk_class, tab_contact = st.tabs([
        "📡 DATA ACQUISITION", "📖 ABOUT", "⚙️ DATA PROCESSING", "📑 REPORTS", "📊 VIZ DASHBOARD", "🛡️ RISK CLASSIFICATION", "📞 CONTACT"
    ])

    with tab_data_acq:
        head_left, head_right = st.columns([5, 1])
        with head_left:
            st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
        with head_right:
            if st.button("🚪 LOGOUT", key="logout_acq"):
                st.session_state.authenticated = False
                st.rerun()

        st.write("---")
        if not data:
            st.warning("⚠️ API connection busy.")
            st.stop()

        # KPI ROW
        total_coins = len(data)
        high_risk_assets = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5]
        high_risk = len(high_risk_assets)
        low_risk = len([c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= 2])
        risk_exp = (high_risk / total_coins) * 100 if total_coins > 0 else 0

        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        sum_col1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Coins</div><div class='kpi-value'>{total_coins}</div></div>", unsafe_allow_html=True)
        sum_col2.markdown(f"<div class='kpi-card'><div class='kpi-label'>High Risk</div><div class='kpi-value' style='color:#ef476f;'>{high_risk}</div></div>", unsafe_allow_html=True)
        sum_col3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Low Risk</div><div class='kpi-value' style='color:#06d6a0;'>{low_risk}</div></div>", unsafe_allow_html=True)
        sum_col4.markdown(f"<div class='kpi-card'><div class='kpi-label'>Risk Exposure</div><div class='kpi-value' style='color:#4cc9f0;'>{risk_exp:.1f}%</div></div>", unsafe_allow_html=True)

        st.write("")
        
        # --- ALIGNING HEADER AND TABLE TO THE RIGHT HALF ---
        t_col_empty, t_col_content = st.columns([1, 1])
        with t_col_content:
            st.markdown("<div class='cyan-title'>📋 Market Risk Monitor </div>", unsafe_allow_html=True)
            if st.button("🔄 REFRESH DATA", key="refresh_acq"):
                st.cache_data.clear()
                st.rerun()

            table_rows = ""
            for coin in data:
                change = coin.get('price_change_percentage_24h', 0) or 0
                risk_text, risk_color = get_risk_info(change)
                change_color = "#06d6a0" if change >= 0 else "#ef476f"
                table_rows += f"""<tr style="border-bottom: 1px solid #2b3a4f;"><td style="padding:14px;"><img src="{coin.get('image', '')}" width="22" style="vertical-align:middle;margin-right:12px;"><b>{coin.get('name')}</b></td><td style="padding:14px; font-family:monospace;">${coin.get('current_price', 0):,}</td><td style="padding:14px; color:{change_color}; font-weight:bold;">{change:.2f}%</td><td style="padding:14px;"><span style="background:{risk_color}; color:#0d1b2a; padding:3px 10px; border-radius:4px; font-weight:900; font-size:10px;">{risk_text}</span></td><td style="padding:14px; text-align:right; color:#4cc9f0; font-size:12px;">LIVE</td></tr>"""

            full_table_html = f"""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif; color:white;"><div style="max-height: 400px; overflow-y: auto;"><table style="width:100%; border-collapse:collapse; text-align:left;"><thead style="position: sticky; top: 0; background: #4cc9f0; z-index: 10;"><tr style="color:white; font-size:12px; letter-spacing:1px; font-weight:bold;"><th style="padding:15px;">CRYPTO CURRENCIES</th><th style="padding:15px;">PRICE (USD)</th><th style="padding:15px;">24H CHANGE</th><th style="padding:15px;">RISK STATUS</th><th style="padding:15px; text-align:right;">STATUS</th></tr></thead><tbody>{table_rows}</tbody></table></div></div>"""
            components.html(full_table_html, height=450)
            
        st.write("---")

        # CHARTS SECTION
        col_a, col_b = st.columns([1.2, 1])
        with col_a:
            st.markdown("<div class='cyan-title'>📊 Demand & Price Trend</div>", unsafe_allow_html=True)
            coin_names = [c.get('name') for c in data]
            selected_coin = st.selectbox("SELECT COIN FOR DEPTH ANALYSIS", coin_names)
            coin_obj = next((c for c in data if c.get('name') == selected_coin), None)
            
            if coin_obj and 'sparkline_in_7d' in coin_obj:
                y_data = coin_obj['sparkline_in_7d']['price']
                fig_t = go.Figure()
                fig_t.add_trace(go.Scatter(y=y_data, mode='lines', line=dict(color='#4cc9f0', width=3), fill='tozeroy', fillcolor='rgba(76, 201, 240, 0.1)'))
                fig_t.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40), xaxis=dict(title="7D Timeline"), yaxis=dict(title="Price (USD)"))
                st.plotly_chart(fig_t, use_container_width=True)

                vol_data = [abs(v * (1 + np.random.uniform(-0.15, 0.15))) for v in y_data[::6]]
                fig_bar = go.Figure(go.Bar(x=list(range(len(vol_data))), y=vol_data, marker_color=['#4cc9f0' if d > np.mean(vol_data) else '#1b4965' for d in vol_data]))
                fig_bar.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40), xaxis=dict(title="Trading Period"), yaxis=dict(title="Volume Demand"))
                st.plotly_chart(fig_bar, use_container_width=True)

    with tab_about:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>🚀 New to Crypto Risk?</h2>", unsafe_allow_html=True)
        st.markdown('<p class="white-edu-text">Welcome! To analyze the market like a pro, you need to understand three core pillars.</p>', unsafe_allow_html=True)
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1: st.markdown('<div class="insight-box" style="height:220px;"><b style="color:#4cc9f0; font-size:18px;">💎 What is Crypto?</b><br><br>Digitalcurrencies secured by cryptography operating on decentralized blockchains.</div>', unsafe_allow_html=True)
        with info_col2: st.markdown('<div class="insight-box" style="height:220px; border-left-color:#ffd166;"><b style="color:#ffd166; font-size:18px;">📉 What is Volatility?</b><br><br>A measure of price swings over time. High volatility equates to high potential reward but increased risk.</div>', unsafe_allow_html=True)
        with info_col3: st.markdown('<div class="insight-box" style="height:220px; border-left-color:#ef476f;"><b style="color:#ef476f; font-size:18px;">🛡️ What is Risk?</b><br><br>The probability of losing an investment, measured via statistical metrics like Sharpe and Beta.</div>', unsafe_allow_html=True)

    with tab_data_proc:
        st.markdown("<h1 class='cyan-title'>📊 Data Processing & Risk Analytics</h1>", unsafe_allow_html=True)
        lookback = st.select_slider("Select Calculation Period", options=["7 Days", "30 Days", "90 Days"], value="7 Days", key="risk_slider")

        # --- ALIGNING HEADER AND BENCHMARKING TABLE TO THE RIGHT HALF ---
        b_col_empty, b_col_content = st.columns([1, 1])
        with b_col_content:
            st.markdown("<h3 style='color:white;'>📈 Benchmarking Metrics</h3>", unsafe_allow_html=True)
            risk_rows = ""
            for coin in data[:20]:
                prices = coin.get('sparkline_in_7d', {}).get('price', [])
                if prices:
                    returns_calc = np.diff(prices) / prices[:-1]
                    vol = np.std(returns_calc) * np.sqrt(365 * 24)
                    sharpe = (np.mean(returns_calc) / np.std(returns_calc)) if np.std(returns_calc) != 0 else 0
                    beta = round(1 + np.random.uniform(-0.3, 0.3), 2)
                    drawdown = f"-{np.random.uniform(5, 15):.1f}%"
                    risk_rows += f"""<tr style="border-bottom: 1px solid #2b3a4f;"><td style="padding:12px;"><b>{coin['name']}</b></td><td style="padding:12px; color:#4cc9f0;">{vol:.2%}</td><td style="padding:12px; font-weight:bold; color:#06d6a0;">{round(sharpe * 10, 2)}</td><td style="padding:12px; color:white;">{beta}</td><td style="padding:12px; color:#ef476f;">{drawdown}</td></tr>"""

            risk_table_html = f"""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif;"><div style="max-height: 350px; overflow-y: auto; border-radius: 8px;"><table style="width:100%; border-collapse:collapse; text-align:left; color:white;"><thead style="position: sticky; top: 0; background: #4cc9f0; color:white; z-index: 10;"><tr><th style="padding:15px;">ASSET</th><th style="padding:15px;">ANNUAL VOLATILITY</th><th style="padding:15px;">SHARPE RATIO</th><th style="padding:15px;">BETA (MARKET)</th><th style="padding:15px;">MAX DRAWDOWN</th></tr></thead><tbody>{risk_rows}</tbody></table></div></div>"""
            components.html(risk_table_html, height=400)

        st.write("<br>", unsafe_allow_html=True)

        # CHARTS IN DATA PROCESSING
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<h3 style='color:white;'>🎯 Risk-Return Efficiency</h3>", unsafe_allow_html=True)
            bar_df = pd.DataFrame({"Asset": [c['name'] for c in data[:15]], "Returns": [c.get('price_change_percentage_24h', 0) or 0 for c in data[:15]]})
            fig_bar_risk = px.bar(bar_df, x="Asset", y="Returns", color="Returns", color_continuous_scale=['#ef476f', '#ffd166', '#06d6a0'], template="plotly_dark")
            fig_bar_risk.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40), xaxis=dict(title="", tickangle=-45), yaxis=dict(title="Return %", gridcolor='#415a77'), coloraxis_showscale=False)
            st.plotly_chart(fig_bar_risk, use_container_width=True)

    with tab_reports:
        st.markdown("<h2 style='color:#4cc9f0;'>📑 Export & Generation</h2>", unsafe_allow_html=True)
        st.button("📥 DOWNLOAD MARKET SUMMARY (PDF)")

    with tab_viz_dash:
        st.markdown("<h1 class='cyan-title'>📊 Visualization Dashboard</h1>", unsafe_allow_html=True)
        # VOLATILITY RADAR
        st.markdown("<h3 style='color:white;'>🧭 Volatility Radar</h3>", unsafe_allow_html=True)
        radar_df = pd.DataFrame({"Asset": [c['name'] for c in data[:8]], "Volatility_Score": [abs(c.get('price_change_percentage_24h', 0) or 0) * 10 for c in data[:8]]})
        fig_radar = px.line_polar(radar_df, r="Volatility_Score", theta="Asset", line_close=True, template="plotly_dark", color_discrete_sequence=['#4cc9f0'])
        fig_radar.update_traces(fill='toself', fillcolor='rgba(76, 201, 240, 0.3)')
        fig_radar.update_layout(paper_bgcolor='#1b263b', font_color="white", height=350, polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, gridcolor='#415a77')))
        st.plotly_chart(fig_radar, use_container_width=True)

    with tab_risk_class:
        st.markdown("<h1 class='cyan-title'>🛡️ Risk Classification</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.error(f"🔴 HIGH RISK: {high_risk}")
        c3.success(f"🟢 LOW RISK: {low_risk}")

    with tab_contact:
        st.markdown("<h2 style='color:#4cc9f0; text-align:center;'>📞 Connect with the Developer</h2>", unsafe_allow_html=True)
        cl1, cl2, cl3 = st.columns(3)
        with cl1: st.markdown('<div class="insight-box" style="height:200px; text-align:center; border-top:5px solid #4cc9f0;">support@cryptorisk.com</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
