import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #1d3557;
    color: #f1faee;
}
[data-testid="stSidebar"] {
    background-color: #457b9d;
}
.metric-card {
    background-color: #457b9d;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}
.metric-card h1 {
    color: #a8dadc;
}
.metric-card h3 {
    color: #f1faee;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------
@st.cache_data(show_spinner=False)
def fetch_crypto_data(limit):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return []

# ---------------- RISK FUNCTION ----------------
def calculate_risk(change):
    if change < 5:
        return "Low"
    elif change < 10:
        return "Medium"
    else:
        return "High"

# ---------------- MAIN APP ----------------
def main():
    st.markdown(
        "<h1 style='color:#a8dadc;'>📈 Cryptocurrency Volatility & Risk Dashboard</h1>",
        unsafe_allow_html=True
    )
    st.caption("Live crypto market analysis using CoinGecko API")

    # Sidebar
    st.sidebar.header("⚙️ Dashboard Controls")
    num_cryptos = st.sidebar.slider("Number of Cryptocurrencies", 10, 100, 50, 10)

    # Fetch Data
    data = fetch_crypto_data(num_cryptos)
    if not data:
        st.error("Unable to fetch data. Please try again later.")
        st.stop()

    # ---------------- PROCESS DATA ----------------
    rows = []
    for coin in data:
        change = coin.get("price_change_percentage_24h") or 0.0

        rows.append({
            "Name": coin.get("name", "N/A"),
            "Symbol": coin.get("symbol", "").upper(),
            "Current Price (USD)": coin.get("current_price", 0),
            "24h Change (%)": round(change, 2),
            "Risk Level": calculate_risk(abs(change))
        })

    df = pd.DataFrame(rows)

    # ---------------- KPI CARDS ----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"<div class='metric-card'><h3>Total Cryptos</h3><h1>{len(df)}</h1></div>",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"<div class='metric-card'><h3>Highest Change</h3><h1>{df['24h Change (%)'].max()}%</h1></div>",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"<div class='metric-card'><h3>High Risk Assets</h3><h1>{len(df[df['Risk Level']=='High'])}</h1></div>",
            unsafe_allow_html=True
        )

    st.divider()

    # ---------------- TABLE ----------------
    st.subheader("📋 Cryptocurrency Market Data")
    st.dataframe(df, use_container_width=True)

    # ---------------- BAR CHART ----------------
    st.subheader("📊 24-Hour Volatility Comparison")
    fig_bar = px.bar(
        df,
        x="Name",
        y="24h Change (%)",
        color="Risk Level",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e74c3c"
        }
    )
    fig_bar.update_layout(
        plot_bgcolor="#1d3557",
        paper_bgcolor="#1d3557",
        font_color="#f1faee"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------- LINE CHART ----------------
    st.subheader("📈 Price Comparison (Top 10)")
    top10 = df.head(10)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=top10["Name"],
        y=top10["Current Price (USD)"],
        mode="lines+markers",
        line=dict(color="#a8dadc", width=3),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        plot_bgcolor="#1d3557",
        paper_bgcolor="#1d3557",
        font_color="#f1faee",
        title="Current Prices of Top 10 Cryptocurrencies"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ---------------- FOOTER ----------------
    st.caption(
        f"Data Source: CoinGecko API | Last Updated: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}"
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
