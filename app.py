import streamlit as st
import requests
import pandas as pd
import plotly.express as px
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
    margin-bottom: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.4);
}
.title {
    font-size: 22px;
    font-weight: bold;
    color: #4dd0e1;
}
.subtext {
    font-size: 13px;
    color: #9ecbff;
}
.metric {
    background-color: #102a43;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.metric h2 {
    color: #4dd0e1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA (SAFE) ----------------
def fetch_crypto_data(limit):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Streamlit Crypto Dashboard)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return []


# ---------------- RISK LOGIC ----------------
def calculate_risk(change):
    if abs(change) < 5:
        return "Low"
    elif abs(change) < 10:
        return "Medium"
    else:
        return "High"

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
num_cryptos = st.sidebar.slider("Number of Cryptocurrencies", 5, 20, 5)

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()


# ---------------- LOAD DATA ----------------
data = fetch_crypto_data(num_cryptos)

if not data:
    st.warning("⚠️ Unable to fetch live data. Please refresh.")
    st.stop()

# ---------------- PROCESS DATA ----------------
rows = []
for coin in data:
    rows.append({
        "Cryptocurrency": coin.get("name", "N/A"),
        "Price (USD)": coin.get("current_price", 0),
        "24h Change (%)": round(coin.get("price_change_percentage_24h") or 0, 2),
        "Risk": calculate_risk(coin.get("price_change_percentage_24h") or 0)
    })

df = pd.DataFrame(rows)

# ---------------- HEADER CARD ----------------
st.markdown("""
<div class="card">
    <span class="title">☁️ Crypto Data Fetcher</span>
    <span style="float:right;color:#2ecc71;">● Live</span><br>
    <span class="subtext">Real-time cryptocurrency market data</span>
</div>
""", unsafe_allow_html=True)

# ---------------- TABLE ----------------

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#4dd0e1;'>📋 Market Overview</h3>", unsafe_allow_html=True)

table_html = """
<style>
.crypto-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.crypto-table th {
    background-color: #0b2a4a;
    color: #4dd0e1;
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #123a5a;
}
.crypto-table td {
    background-color: #071e33;
    color: #e6f1ff;
    padding: 10px;
    border-bottom: 1px solid #123a5a;
}
.crypto-table tr:hover td {
    background-color: #0b2a4a;
}
.risk-low { color: #2ecc71; font-weight: bold; }
.risk-medium { color: #f1c40f; font-weight: bold; }
.risk-high { color: #e74c3c; font-weight: bold; }
</style>

<table class="crypto-table">
<tr>
    <th>Cryptocurrency</th>
    <th>Price (USD)</th>
    <th>24h Change (%)</th>
    <th>Risk</th>
</tr>
"""

for _, row in df.iterrows():
    risk_class = (
        "risk-low" if row["Risk"] == "Low"
        else "risk-medium" if row["Risk"] == "Medium"
        else "risk-high"
    )

    table_html += f"""
    <tr>
        <td>{row['Cryptocurrency']}</td>
        <td>${row['Price (USD)']}</td>
        <td>{row['24h Change (%)']}%</td>
        <td class="{risk_class}">{row['Risk']}</td>
    </tr>
    """

table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)



# ---------------- METRICS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='metric'><h3>Total Assets</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric'><h3>Highest Change</h3><h2>{df['24h Change (%)'].max()}%</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric'><h3>High Risk</h3><h2>{len(df[df['Risk']=='High'])}</h2></div>", unsafe_allow_html=True)

# ---------------- BAR CHART ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 24-Hour Volatility Comparison")

fig = px.bar(
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
fig.update_layout(
    plot_bgcolor="#071e33",
    paper_bgcolor="#071e33",
    font_color="#e6f1ff"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.caption(
    f"Data Source: CoinGecko API | Last Updated: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}"
)
