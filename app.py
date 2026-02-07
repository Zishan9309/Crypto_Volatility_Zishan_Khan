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
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
h1 {
    text-align: center;
    color: #00e5ff;
}
.sub {
    text-align: center;
    color: #cfd8dc;
    font-size: 18px;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.low { color: #00e676; font-weight: bold; }
.medium { color: #ffea00; font-weight: bold; }
.high { color: #ff5252; font-weight: bold; }
.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>💹 Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Live Online Crypto Data • Streamlit Project</div>", unsafe_allow_html=True)

st.write("")

# ---------------- FETCH ONLINE DATA ----------------
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
coins = response.json()

crypto_rows = []

for coin in coins:
    change = coin["price_change_percentage_24h"]

    if change >= 10:
        risk = "High"
        risk_class = "high"
    elif change >= 5:
        risk = "Medium"
        risk_class = "medium"
    else:
        risk = "Low"
        risk_class = "low"

    crypto_rows.append({
        "Crypto": coin["name"],
        "Symbol": coin["symbol"].upper(),
        "Price ($)": coin["current_price"],
        "24h Change (%)": round(change, 2),
        "Risk": f"{risk}"
    })

df = pd.DataFrame(crypto_rows)

# ---------------- METRIC CARDS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='card'>💰<br><h2>Total Cryptos</h2><h1>5</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(
        f"<div class='card'>📈<br><h2>Highest Change</h2><h1>{df['24h Change (%)'].max()}%</h1></div>",
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"<div class='card'>⚠️<br><h2>High Risk Coins</h2><h1>{len(df[df['Risk']=='High'])}</h1></div>",
        unsafe_allow_html=True
    )

st.write("")

# ---------------- TABLE WITH ICONS ----------------
st.subheader("📊 Live Crypto Market Table")

for _, row in df.iterrows():
    st.markdown(
        f"""
        <div class="card" style="margin-bottom:15px;">
            <h3>🪙 {row['Crypto']} ({row['Symbol']})</h3>
            💲 Price: <b>${row['Price ($)']}</b><br>
            📉 24h Change: <b>{row['24h Change (%)']}%</b><br>
            ⚠️ Risk Level: <span class="{row['Risk'].lower()}">{row['Risk']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- FOOTER ----------------
st.write("")
st.markdown(
    "<div class='footer'>Developed using Streamlit | Infosys Springboard Project</div>",
    unsafe_allow_html=True
)
