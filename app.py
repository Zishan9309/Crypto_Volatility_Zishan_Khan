import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="💹",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0b132b, #1c2541, #3a506b);
    color: #eaeaea;
}
h1 {
    text-align: center;
    color: #5bc0eb;
}
.sub {
    text-align: center;
    color: #b0bec5;
    font-size: 18px;
}
.card {
    background-color: #1c2541;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.low { color: #3ddc97; font-weight: bold; }
.medium { color: #f4d35e; font-weight: bold; }
.high { color: #ff6b6b; font-weight: bold; }
.footer {
    text-align: center;
    color: #b0bec5;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>💹 Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Live Interactive Dashboard using Online Crypto Data</div>", unsafe_allow_html=True)
st.write("")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
num_coins = st.sidebar.slider("Number of Cryptos", 3, 10, 5)
st.sidebar.caption("Data Source: CoinGecko API")

# ---------------- FETCH DATA SAFELY ----------------
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

coins = fetch_crypto_data(num_coins)

# ---------------- PROCESS DATA (SAFE) ----------------
rows = []

for coin in coins:
    change = coin.get("price_change_percentage_24h")

    if change is None:
        change = 0.0

    if change >= 10:
        risk = "High"
    elif change >= 5:
        risk = "Medium"
    else:
        risk = "Low"

    rows.append({
        "Crypto": coin.get("name", "N/A"),
        "Symbol": coin.get("symbol", "").upper(),
        "Price (USD)": coin.get("current_price", 0),
        "24h Change (%)": round(change, 2),
        "Risk Level": risk
    })

df = pd.DataFrame(rows)

# ---------------- METRICS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🪙 Cryptos", len(df))
with c2:
    st.metric("📈 Max Change (%)", df["24h Change (%)"].max() if not df.empty else 0)
with c3:
    st.metric("⚠️ High Risk", len(df[df["Risk Level"] == "High"]))

st.write("---")

# ---------------- TABLE ----------------
st.subheader("📋 Live Crypto Market Data")
st.dataframe(df, use_container_width=True)

# ---------------- CHART ----------------
st.subheader("📊 Volatility Comparison")
if not df.empty:
    st.bar_chart(df.set_index("Crypto")["24h Change (%)"])
else:
    st.warning("No data available at the moment.")

# ---------------- FOOTER ----------------
st.write("---")
st.markdown(
    "<div class='footer'>Infosys Springboard | Streamlit Interactive Crypto Dashboard</div>",
    unsafe_allow_html=True
)
