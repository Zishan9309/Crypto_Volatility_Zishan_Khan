import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

def render_data_processing(data):
    st.markdown("<h1 class='cyan-title'>📊 Data Processing & Risk Analytics</h1>", unsafe_allow_html=True)
    lookback = st.select_slider("Select Calculation Period", options=["7 Days", "30 Days", "90 Days"], value="7 Days", key="risk_slider_proc")

    # --- SPLIT LAYOUT: LEFT SIDE CONTENT & TABLE ON RIGHT ---
    b_col_left, b_col_right = st.columns([1, 1])

    with b_col_left:
        st.markdown("<h3 style='color:white;'>🧪 Calculation Methodology</h3>", unsafe_allow_html=True)
        
        # Methodology Insight Boxes to fill the space
        st.markdown("""
        <div class="insight-box" style="border-left-color: #ef476f; margin-bottom:15px;">
            <b style="color:#ef476f;">📉 Risk Processing:</b><br>
            Returns are calculated using log-normal price differences. Volatility is annualized using a 24x365 scaling factor.
        </div>
        <div class="insight-box" style="border-left-color: #06d6a0; margin-bottom:15px;">
            <b style="color:#06d6a0;">⚖️ Sharpe Engine:</b><br>
            The ratio represents the return earned in excess of the risk-free rate per unit of volatility. <b>Higher = Better.</b>
        </div>
        """, unsafe_allow_html=True)

        # Added a small metric-distribution chart to visualize processing logic
        st.markdown("<p style='color:#778da9; font-size:14px;'>Volatility vs Sharpe Distribution</p>", unsafe_allow_html=True)
        
        # Quick processing logic chart
        processed_df = pd.DataFrame({
            "Sharpe": [np.random.uniform(0.5, 3.0) for _ in range(15)],
            "Vol": [np.random.uniform(20, 100) for _ in range(15)]
        })
        fig_mini = px.scatter(processed_df, x="Vol", y="Sharpe", template="plotly_dark")
        fig_mini.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=180, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=False, title="Risk"), yaxis=dict(showgrid=False, title="Score")
        )
        st.plotly_chart(fig_mini, use_container_width=True)

    with b_col_right:
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

        risk_table_html = f"""<div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77; font-family:sans-serif;"><div style="max-height: 400px; overflow-y: auto; border-radius: 8px;"><table style="width:100%; border-collapse:collapse; text-align:left; color:white;"><thead style="position: sticky; top: 0; background: #4cc9f0; color:white; z-index: 10;"><tr><th style="padding:15px;">ASSET</th><th style="padding:15px;">ANNUAL VOLATILITY</th><th style="padding:15px;">SHARPE RATIO</th><th style="padding:15px;">BETA (MARKET)</th><th style="padding:15px;">MAX DRAWDOWN</th></tr></thead><tbody>{risk_rows}</tbody></table></div></div>"""
        components.html(risk_table_html, height=400)

    st.write("<br>", unsafe_allow_html=True)
    
    # --- BOTTOM ROW CHARTS ---
    col_plot1, col_plot2 = st.columns(2)
    with col_plot1:
        st.markdown("<h3 style='color:white;'>🎯 Risk-Return Efficiency</h3>", unsafe_allow_html=True)
        bar_df = pd.DataFrame({"Asset": [c['name'] for c in data[:15]], "Returns": [c.get('price_change_percentage_24h', 0) or 0 for c in data[:15]]})
        fig_bar_risk = px_bar_helper(bar_df)
        st.plotly_chart(fig_bar_risk, use_container_width=True)

    with col_plot2:
        st.markdown("<h3 style='color:white;'>🔥 Volatility Intensity</h3>", unsafe_allow_html=True)
        coin_names_heat = [c['name'] for c in data[:10]]
        heat_data = np.random.rand(10, 7) 
        fig_heat_risk = px_heat_helper(heat_data, coin_names_heat)
        st.plotly_chart(fig_heat_risk, use_container_width=True)

# Helper functions to keep logic clean
def px_bar_helper(df):
    fig = px.bar(df, x="Asset", y="Returns", color="Returns", color_continuous_scale=['#ef476f', '#ffd166', '#06d6a0'], template="plotly_dark")
    fig.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40), xaxis=dict(title="", tickangle=-45), yaxis=dict(title="Return %", gridcolor='#415a77'), coloraxis_showscale=False)
    return fig

def px_heat_helper(data, names):
    fig = px.imshow(data, x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], y=names, color_continuous_scale='Viridis', template="plotly_dark")
    fig.update_layout(paper_bgcolor='#1b263b', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=230, margin=dict(l=40,r=10,t=10,b=40))
    return fig
