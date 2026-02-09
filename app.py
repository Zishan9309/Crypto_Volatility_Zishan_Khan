import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration for dark theme
st.set_page_config(
    page_title="Crypto Volatility Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# Crypto Volatility Dashboard\nBuilt with Streamlit for analyzing crypto risk."
    }
)

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
    }
    .stDataFrame {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to fetch data from CoinGecko API
def fetch_crypto_data(limit=50):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false&price_change_percentage=24h"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Function to calculate risk level based on 24h price change percentage
def calculate_risk_level(price_change_pct):
    if abs(price_change_pct) < 5:
        return "Low"
    elif abs(price_change_pct) < 10:
        return "Medium"
    else:
        return "High"

# Function to get color for risk level
def get_risk_color(risk):
    if risk == "Low":
        return "green"
    elif risk == "Medium":
        return "orange"
    else:
        return "red"

# Main app
def main():
    st.title("📈 Cryptocurrency Volatility & Risk Dashboard")
    st.markdown("Analyze live crypto market data with interactive visualizations.")

    # Sidebar controls
    st.sidebar.header("Controls")
    num_cryptos = st.sidebar.slider("Select Number of Cryptocurrencies", min_value=10, max_value=100, value=50, step=10)
    refresh = st.sidebar.button("Refresh Data")

    # Fetch data
    if 'data' not in st.session_state or refresh:
        st.session_state.data = fetch_crypto_data(num_cryptos)
    
    data = st.session_state.data
    if not data:
        st.stop()

    # Process data into DataFrame
    df = pd.DataFrame(data)
    df = df[['name', 'symbol', 'current_price', 'price_change_percentage_24h']]
    df.columns = ['Name', 'Symbol', 'Current Price (USD)', '24h Change (%)']
    df['Risk Level'] = df['24h Change (%)'].apply(calculate_risk_level)
    df['Risk Color'] = df['Risk Level'].apply(get_risk_color)

    # KPIs
    total_cryptos = len(df)
    highest_change = df['24h Change (%)'].max()
    high_risk_count = len(df[df['Risk Level'] == 'High'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Cryptocurrencies</h3>
            <h1>{total_cryptos}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Highest 24h Change (%)</h3>
            <h1>{highest_change:.2f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>High-Risk Count</h3>
            <h1>{high_risk_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Data Table
    st.subheader("Cryptocurrency Data Table")
    st.dataframe(
        df.style.apply(lambda x: [f'background-color: {get_risk_color(x["Risk Level"])}' if col == 'Risk Level' else '' for col in x.index], axis=1),
        use_container_width=True
    )

    # Charts
    st.subheader("Volatility Comparison Charts")

    # Bar Chart for 24h Change
    fig_bar = px.bar(
        df, x='Name', y='24h Change (%)',
        title="24-Hour Price Change Percentage",
        color='Risk Level',
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    )
    fig_bar.update_layout(
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font_color='white',
        xaxis_title="Cryptocurrency",
        yaxis_title="24h Change (%)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart for Top 10 by Market Cap (using current price as proxy for trend)
    top_10 = df.head(10)
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=top_10['Name'],
        y=top_10['Current Price (USD)'],
        mode='lines+markers',
        name='Current Price',
        line=dict(color='cyan')
    ))
    fig_line.update_layout(
        title="Current Prices of Top 10 Cryptocurrencies",
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font_color='white',
        xaxis_title="Cryptocurrency",
        yaxis_title="Price (USD)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("Data sourced from CoinGecko API. Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
