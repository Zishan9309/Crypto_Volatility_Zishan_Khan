import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📈",
    layout="wide"
)

# ---------------- INITIALIZE SESSION STATE ----------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ---------------- CSS: MAIN DIV & LOGIN FORM STYLING ----------------
st.markdown("""
<style>
    /* Main Body Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* Centering the Login Container */
    .main-login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }

    /* The Main Login Form Div */
    .login-form-div {
        background-color: #1b263b;
        padding: 45px;
        border-radius: 15px;
        border: 2px solid #4cc9f0; /* Aesthetic Cyan Border */
        width: 100%;
        max-width: 400px;
        box-shadow: 0px 0px 25px rgba(76, 201, 240, 0.3);
        text-align: center;
    }

    .form-heading {
        color: #4cc9f0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Text Field Label Styling */
    .field-label {
        color: #778da9;
        text-align: left;
        display: block;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    /* Login Button Customization */
    div.stButton > button {
        background-color: #4cc9f0 !important;
        color: #0d1b2a !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        margin-top: 15px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        box-shadow: 0px 0px 15px #4cc9f0;
        transform: scale(1.02);
    }

    /* Input Box Overrides */
    input {
        background-color: #0d1b2a !important;
        color: white !important;
        border: 1px solid #415a77 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE FUNCTION ----------------
def login_page():
    # Vertical spacer to push form to middle
    st.write("#")
    st.write("#")
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        # Wrapping everything in the styled 'login-form-div'
        st.markdown('<div class="login-form-div">', unsafe_allow_html=True)
        st.markdown('<h2 class="form-heading">System Access</h2>', unsafe_allow_html=True)
        
        # Username Field
        st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
        username = st.text_input("User", label_visibility="collapsed", placeholder="Enter admin ID")
        
        st.write("") # Spacer
        
        # Password Field
        st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        # Login Button
        if st.button("LOGIN TO DASHBOARD"):
            if username == "admin" and password == "crypto123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Login Credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE FUNCTION ----------------
def dashboard_page():
    # Heading
    st.markdown("<h1 style='color:#4cc9f0;'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
    
    # Sidebar Logout
    if st.sidebar.button("🚪 LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- Fetching Real Data (Milestone 1) ---
    @st.cache_data(ttl=60)
    def fetch_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "sparkline": "true"}
        try: return requests.get(url, params=params).json()
        except: return []

    data = fetch_data()

    # --- Scrollable Table (Milestone 1) ---
    table_rows = ""
    for coin in data:
        change = coin.get('price_change_percentage_24h', 0) or 0
        table_rows += f"""
        <tr style="border-bottom: 1px solid #2b3a4f; color:white;">
            <td style="padding:12px;">{coin['name']}</td>
            <td style="padding:12px;">${coin['current_price']:,}</td>
            <td style="padding:12px;">{change:.2f}%</td>
        </tr>"""

    table_html = f"""
    <div style="background:#1b263b; padding:15px; border-radius:12px; border:1px solid #415a77;">
        <table style="width:100%; border-collapse:collapse; color:white;">
            <thead style="color:#778da9; font-size:12px; border-bottom: 2px solid #415a77;">
                <tr><th style="text-align:left;">ASSET</th><th style="text-align:left;">PRICE</th><th style="text-align:left;">CHANGE</th></tr>
            </thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>"""
    components.html(table_html, height=400)

# ---------------- MAIN APP FLOW ----------------
if st.session_state['logged_in']:
    dashboard_page()
else:
    login_page()
