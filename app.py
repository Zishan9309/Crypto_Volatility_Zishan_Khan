import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="💹",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
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
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.4);
}

.low {
    color: #3ddc97;
    font-weight: bold;
}

.medium {
    color: #f4d35e;
    font-weight: bold;
}

.high {
    color: #ff6b6b;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #b0bec5;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown("<h1>💹 Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Interactive Dashboard using Live Online Data</div>", unsafe_allow_html=True)

st.write("")

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("⚙️ Dashboard Controls")

num_coins = st.sidebar.slider(
    "Select number of cryptocurrencies",
    min_value=3,
    max_value=10,
    value=5
)

risk_filter = st.sidebar.multiselect(
    "Filter by Risk Level",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

st.sidebar.write("Data Source: CoinGecko API")

# ---------------- FETCH ONLINE DATA ----------------
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": num_coins,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
coins = response.json()

crypto_data = []

for coin in coins:
    change = coin["price_change_percentage_24h"]

    if change >= 10:
        risk = "High"
    elif change >= 5:
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

# ---------------- APPLY FILTER ----------------
df = df[df["Risk Level"].isin(risk_filter)]

# ---------------- KPI METRICS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🪙 Cryptos Displayed", len(df))

with c2:
    if not df.empty:
        st.metric("📈 Highest Change (%)", df["24h Change (%)"].max())
    else:
        st.metric("📈 Highest Change (%)", "N/A")

with c3:
    st.metric("⚠️ High Risk Count", len(df[df["Risk Level"] == "High"]))

st.write("---")

# ---------------- DATA TABLE ----------------
st.subheader("📋 Live Crypto Market Table")
st.dataframe(df, use_container_width=True)

# ---------------- INTERACTIVE CHART ----------------
st.subheader("📊 Volatility Comparison Chart")
if not df.empty:
    st.bar_chart(
        data=df.set_index("Crypto")["24h Change (%)"]
    )
else:
    st.warning("No data available for selected filters.")

# ---------------- FOOTER ----------------
st.write("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>Infosys Springboard | Streamlit Interactive Dashboard</p>",
    unsafe_allow_html=True
)
