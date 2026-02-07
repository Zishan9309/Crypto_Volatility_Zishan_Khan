import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #35d3ff; text-align: center; }
    .metric-box {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown("<h1>📊 Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>Live Online Crypto Data using CoinGecko API</p>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------- FETCH ONLINE CRYPTO DATA ----------------
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
data = response.json()

# ---------------- PROCESS DATA ----------------
crypto_data = []

for coin in data:
    change = coin["price_change_percentage_24h"]

    if change > 10:
        risk = "High"
    elif change > 5:
        risk = "Medium"
    else:
        risk = "Low"

    crypto_data.append({
        "Crypto": coin["name"],
        "Symbol": coin["symbol"].upper(),
        "Price (USD)": coin["current_price"],
        "24h Change (%)": round(change, 2),
        "Risk Level": risk
    })

df = pd.DataFrame(crypto_data)

# ---------------- DISPLAY METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Cryptos Tracked", len(df))
with col2:
    st.metric("📈 Highest Change (%)", df["24h Change (%)"].max())
with col3:
    st.metric("⚠️ High Risk Coins", len(df[df["Risk Level"] == "High"]))

st.write("---")

# ---------------- DISPLAY TABLE ----------------
st.subheader("📋 Live Crypto Market Data")
st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.write("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>Infosys Springboard | Streamlit Project</p>",
    unsafe_allow_html=True
)
