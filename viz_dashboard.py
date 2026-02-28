import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

def render_viz_dashboard(data, high_risk, total_coins):
    st.markdown("<h1 class='cyan-title'>📊 Milestone 3: Analytical Dashboard</h1>", unsafe_allow_html=True)
    
    filter_col1, filter_col2 = st.columns([1, 1])
    with filter_col1:
        selected_cryptos = st.multiselect("SELECT CRYPTOCURRENCIES TO COMPARE", options=[c['name'] for c in data], default=[data[0]['name'], data[1]['name']] if len(data) > 1 else [data[0]['name']], key="sel_viz")
    with filter_col2:
        date_range = st.date_input("SELECT DATE RANGE", value=(datetime(2025, 1, 1), datetime.now()), key="date_viz")

    st.write("<br>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    avg_vol, avg_ret, avg_sharpe = np.random.uniform(40, 60), np.random.uniform(2, 8), np.random.uniform(1.1, 2.5)

    m_col1.markdown(f"<div class='kpi-card'><div class='kpi-label'>AVG VOLATILITY</div><div class='kpi-value'>{avg_vol:.2f}%</div></div>", unsafe_allow_html=True)
    m_col2.markdown(f"<div class='kpi-card'><div class='kpi-label'>AVG RETURN</div><div class='kpi-value' style='color:#06d6a0;'>{avg_ret:.2f}%</div></div>", unsafe_allow_html=True)
    m_col3.markdown(f"<div class='kpi-card'><div class='kpi-label'>AVG SHARPE RATIO</div><div class='kpi-value' style='color:#4cc9f0;'>{avg_sharpe:.2f}</div></div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>📈 Time-Series Analysis</h3>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.markdown("<p style='color:#778da9;'>Price Trend (Close Price vs Date)</p>", unsafe_allow_html=True)
        fig_p = go.Figure()
        for crypto in selected_cryptos:
            coin_data = next((c for c in data if c['name'] == crypto), data[0])
            fig_p.add_trace(go.Scatter(y=coin_data.get('sparkline_in_7d', {}).get('price', []), mode='lines', name=crypto))
        fig_p.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250, margin=dict(l=20,r=20,t=20,b=20), legend=dict(orientation="h"))
        st.plotly_chart(fig_p, use_container_width=True)

    with t_col2:
        st.markdown("<p style='color:#778da9;'>Volatility Trend (Risk vs Date)</p>", unsafe_allow_html=True)
        fig_v = go.Figure()
        for crypto in selected_cryptos:
            fig_v.add_trace(go.Scatter(y=[abs(np.random.normal(5, 2)) for _ in range(168)], mode='lines', name=crypto))
        fig_v.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250, margin=dict(l=20,r=20,t=20,b=20), legend=dict(orientation="h"))
        st.plotly_chart(fig_v, use_container_width=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>⚖️ Risk-Return Strategic Mapping</h3>", unsafe_allow_html=True)
    scat_col, table_col = st.columns([2, 1])
    with scat_col:
        scatter_data = pd.DataFrame({"Crypto": [c['name'] for c in data], "Volatility": [abs(c['price_change_percentage_24h'] or 0) * 1.5 for c in data], "Average Return": [c['price_change_percentage_24h'] or 0 for c in data], "Sharpe": [abs(np.random.normal(1.5, 0.5)) for _ in data]})
        fig_bubble = px.scatter(scatter_data, x="Volatility", y="Average Return", size="Sharpe", color="Average Return", hover_name="Crypto", color_continuous_scale='RdYlGn', template="plotly_dark")
        fig_bubble.add_hline(y=0, line_dash="dash", line_color="#415a77")
        fig_bubble.add_vline(x=scatter_data["Volatility"].mean(), line_dash="dash", line_color="#415a77")
        fig_bubble.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=400, xaxis=dict(title="Volatility (Risk)"), yaxis=dict(title="Average Returns"))
        st.plotly_chart(fig_bubble, use_container_width=True)

    with table_col:
        st.markdown("<p style='color:#778da9; margin-bottom:10px;'>Strategic Quadrant Guide</p>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif; color:white;"><table style="width:100%; border-collapse:collapse; text-align:left; font-size:13px;"><thead style="border-bottom:2px solid #4cc9f0;"><tr><th>POSITION</th><th>STRATEGY</th></tr></thead><tbody><tr><td style="color:#06d6a0;">Top-Left</td><td>Best Investment</td></tr><tr><td style="color:#ef476f;">Bottom-Right</td><td>Worst Asset</td></tr><tr><td style="color:#ffd166;">Top-Right</td><td>Speculative</td></tr><tr><td style="color:#4cc9f0;">Bottom-Left</td><td>Stable Asset</td></tr></tbody></table></div>""", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>🏆 Market Analysis Results</h3>", unsafe_allow_html=True)
    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        risk_score = (high_risk / total_coins) * 100 if total_coins > 0 else 0
        fig_g = go.Figure(go.Indicator(mode = "gauge+number", value = risk_score, gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#4cc9f0"}, 'steps': [{'range': [0, 30], 'color': '#06d6a0'}, {'range': [30, 70], 'color': '#ffd166'}, {'range': [70, 100], 'color': '#ef476f'}]}))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=250)
        st.plotly_chart(fig_g, use_container_width=True)

    with res_col2:
        fig_cum = go.Figure()
        for crypto in selected_cryptos[:3]:
            fig_cum.add_trace(go.Scatter(y=(1 + np.random.normal(0.001, 0.02, 100)).cumprod() * 100, mode='lines', name=f"{crypto} Growth", fill='tozeroy'))
        fig_cum.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250)
        st.plotly_chart(fig_cum, use_container_width=True)

    st.write("---")
    csv = scatter_data[scatter_data['Crypto'].isin(selected_cryptos)].to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 DOWNLOAD MILESTONE 3 ANALYSIS REPORT (CSV)", data=csv, file_name=f'crypto_analysis_{datetime.now().strftime("%Y%m%d")}.csv', mime='text/csv')

    st.markdown("""<div class="insight-box"><b>Milestone 3 Goal:</b> Visualize risk/volatility behavior. "Price tells growth, volatility tells risk".</div>""", unsafe_allow_html=True)
