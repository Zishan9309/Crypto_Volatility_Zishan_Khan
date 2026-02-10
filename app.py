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
        "User-Agent": "Mozilla/5.0 (Crypto Dashboard)"
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return []

st.markdown("""
<style>
.market-card {
    background: linear-gradient(145deg, #071e33, #0b2a4a);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.market-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #e6f1ff;
    margin-bottom: 15px;
}

.market-header h3 {
    color: #4dd0e1;
    margin: 0;
}

.live-dot {
    color: #2ecc71;
    font-size: 14px;
}

.market-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.market-table th {
    color: #9ecbff;
    font-weight: 600;
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #123a5a;
}

.market-table td {
    padding: 12px 10px;
    border-bottom: 1px solid #102a43;
    color: #e6f1ff;
}

.market-table tr:hover td {
    background-color: rgba(77,208,225,0.08);
}

.coin {
    display: flex;
    align-items: center;
    gap: 10px;
}

.coin-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: #4dd0e1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #071e33;
    font-weight: bold;
}

.positive { color: #2ecc71; }
.negative { color: #e74c3c; }

.risk-low {
    background-color: rgba(46,204,113,0.15);
    color: #2ecc71;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

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
num_cryptos = st.sidebar.slider("Number of Cryptocurrencies", 5, 20, 8)

if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# ---------------- LOAD DATA ----------------
data = fetch_crypto_data(num_cryptos)

if not data:
    st.warning("⚠️ Unable to fetch live data. Please refresh.")
    st.stop()

# ---------------- PROCESS DATA ----------------
rows = []
for coin in data:
    change = coin.get("price_change_percentage_24h") or 0
    rows.append({
        "Cryptocurrency": coin.get("name", "N/A"),
        "Price (USD)": coin.get("current_price", 0),
        "24h Change (%)": round(change, 2),
        "Risk": calculate_risk(change)
    })

df = pd.DataFrame(rows)

# ---------------- HEADER CARD ----------------
st.markdown("""
<div class="card">
    <span class="title">☁️ Crypto Data Fetcher</span>
    <span style="float:right;color:#2ecc71;">● Live</span><br>
    <span class="subtext">Real-time cryptocurrency market overview</span>
</div>
""", unsafe_allow_html=True)

# ---------------- MARKET OVERVIEW TABLE ----------------
st.markdown("""
<div class="market-card">
    <div class="market-header">
        <h3>☁️ Crypto Data Fetcher</h3>
        <span class="live-dot">● Live</span>
    </div>

    <table class="market-table">
        <thead>
            <tr>
                <th>Cryptocurrency</th>
                <th>Price (USD)</th>
                <th>24h Change</th>
                <th>Risk</th>
            </tr>
        </thead>
        <tbody>
""", unsafe_allow_html=True)

for coin in data:
    name = coin["name"]
    symbol = coin["symbol"].upper()
    price = coin["current_price"]
    change = coin["price_change_percentage_24h"] or 0

    change_class = "positive" if change >= 0 else "negative"

    st.markdown(f"""
        <tr>
            <td>
                <div class="coin">
                    <div class="coin-icon">{symbol[0]}</div>
                    {name} ({symbol})
                </div>
            </td>
            <td>${price}</td>
            <td class="{change_class}">{change:.2f}%</td>
            <td><span class="risk-low">Low</span></td>
        </tr>
    """, unsafe_allow_html=True)

st.markdown("""
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)


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
