import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# ================= CUSTOM CSS (REFERENCE STYLE) =================
st.markdown("""
<style>
body {
    background-color: #0b1c2d;
    color: #e6f1ff;
}
.navbar {
    background-color: #071521;
    padding: 15px 30px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.nav-title {
    font-size: 22px;
    font-weight: bold;
    color: #4dd0e1;
}
.nav-links {
    float: right;
    color: #9ecbff;
    font-size: 14px;
}
.section-box {
    background-color: #071e33;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.metric-card {
    background-color: #0c2a44;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.low { color: #2ecc71; }
.medium { color: #f1c40f; }
.high { color: #e74c3c; }
</style>
""", unsafe_allow_html=True)

# ================= NAVIGATION BAR =================
st.markdown("""
<div class="navbar">
    <span class="nav-title">📊 Crypto Volatility & Risk Analyzer</span>
    <span class="nav-links">Data Acquisition | Analysis | Visualization</span>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")
num_coins = st.sidebar.slider("Number of Cryptocurrencies", 5, 20, 5)
st.sidebar.caption("Source: CoinGecko API")

# ================= FETCH DATA (SAFE) =================
@st.cache_data(show_spinner=False)
def fetch_data(limit):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return []

data = fetch_data(num_coins)
if not data:
    st.error("Unable to fetch data at the moment.")
    st.stop()

# ================= PROCESS DATA =================
rows = []
for coin in data:
    change = coin.get("price_change_percentage_24h") or 0

    if abs(change) < 5:
        risk = "Low"
    elif abs(change) < 10:
        risk = "Medium"
    else:
        risk = "High"

    rows.append({
        "Cryptocurrency": coin.get("name"),
        "Price (USD)": coin.get("current_price"),
        "24h Change (%)": round(change, 2),
        "Risk Level": risk
    })

df = pd.DataFrame(rows)

# ================= MILESTONE SECTION =================
st.markdown("""
<div class="section-box">
    <h3>Milestone 1: Data Acquisition</h3>
    <ul>
        <li>API integration using CoinGecko</li>
        <li>Live cryptocurrency price data</li>
        <li>Missing value handling</li>
        <li>Structured tabular format</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ================= METRICS =================
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-card'><h4>Total Cryptos</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><h4>Highest Change</h4><h2>{df['24h Change (%)'].max()}%</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><h4>High Risk</h4><h2>{len(df[df['Risk Level']=='High'])}</h2></div>", unsafe_allow_html=True)

# ================= TABLE =================
st.markdown("<div class='section-box'><h3>Crypto Market Table</h3></div>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# ================= CHARTS =================
st.markdown("<div class='section-box'><h3>7-Day Volatility Snapshot</h3></div>", unsafe_allow_html=True)
st.bar_chart(df.set_index("Cryptocurrency")["24h Change (%)"])

# ================= FOOTER =================
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Infosys Springboard Project")
