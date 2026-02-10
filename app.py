import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Data Fetcher",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0b1c2d;
    color: #e6f1ff;
}
[data-testid="stSidebar"] {
    background-color: #102a43;
}
.card {
    background-color: #071e33;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
}
.card-title {
    font-size: 22px;
    font-weight: bold;
    color: #4dd0e1;
}
.card-sub {
    font-size: 13px;
    color: #9ecbff;
}
.refresh-btn button {
    background-color: #1c7ed6;
    color: white;
    border-radius: 8px;
}
.metric {
    background-color: #102a43;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------
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
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except:
        return []

# ---------------- RISK FUNCTION ----------------
def calculate_risk(change):
    if abs(change) < 5:
        return "Low"
    elif abs(change) < 10:
        return "Medium"
    else:
        return "High"

# ---------------- MAIN ----------------
st.sidebar.header("⚙️ Controls")
num_cryptos = st.sidebar.slider("Number of Cryptocurrencies", 5, 20, 5)

# Refresh logic
if "refresh" not in st.session_state:
    st.session_state.refresh = 0

if st.sidebar.button("🔄 Refresh Data"):
    st.session_state.refresh += 1

data = fetch_crypto_data(num_cryptos)

if not data:
    st.error("Failed to fetch crypto data.")
    st.stop()

# ---------------- PROCESS DATA ----------------
rows = []
for coin in data:
    change = coin.get("price_change_percentage_24h") or 0
    rows.append({
        "Cryptocurrency": coin.get("name"),
        "Price (USD)": coin.get("current_price"),
        "24h Change (%)": round(change, 2),
        "Risk": calculate_risk(change)
    })

df = pd.DataFrame(rows)

# ---------------- HEADER CARD (LIKE IMAGE) ----------------
st.markdown("""
<div class="card">
    <span class="card-title">☁️ Crypto Data Fetcher</span>
    <span style="float:right;color:#2ecc71;">● Live</span><br>
    <span class="card-sub">Last updated just now</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- TABLE CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Cryptocurrency Market Overview")
st.dataframe(df, use_container_width=True, height=280)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- METRICS ----------------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric'><h3>Total Assets</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric'><h3>Highest Change</h3><h2>{df['24h Change (%)'].max()}%</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric'><h3>High Risk</h3><h2>{len(df[df['Risk']=='High'])}</h2></div>", unsafe_allow_html=True)

st.write("")

# ---------------- BAR CHART ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Volatility Comparison")
fig_bar = px.bar(
    df,
    x="Cryptocurrency",
    y="24h Change (%)",
    color="Risk",
    color_discrete_map={
        "Low": "#2ecc71",
        "Medium": "#f1c40f",
        "High": "#e74c3c"
    }
)
fig_bar.update_layout(
    plot_bgcolor="#071e33",
    paper_bgcolor="#071e33",
    font_color="#e6f1ff"
)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.caption(f"Data Source: CoinGecko API | {datetime.now().strftime('%d %b %Y %H:%M:%S')}")
