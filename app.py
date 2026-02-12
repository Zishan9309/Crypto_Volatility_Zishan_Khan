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

# ---------------- SESSION STATE ----------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ---------------- CLEANED CSS ----------------
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #0d1b2a !important; }
    
    /* Center the Login Card vertically and horizontally */
    [data-testid="stVerticalBlock"] > div:has(.login-box) {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .login-box {
        background-color: #1b263b;
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #4cc9f0;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 0 25px rgba(76, 201, 240, 0.2);
        margin: auto;
    }
    
    .cyan-title {
        color: #4cc9f0 !important;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 25px;
        line-height: 1.2;
    }

    .input-label {
        color: #778da9;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
        font-size: 12px;
        letter-spacing: 1px;
    }

    /* Remove extra padding from Streamlit widgets */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef);
        color: #0d1b2a !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px !important;
        margin-top: 20px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------
def login_page():
    # Use columns just to center the width
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        # Creating the login container
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="cyan-title">System Access</h2>', unsafe_allow_html=True)
        
        # Using a form to group inputs and prevent accidental refreshes
        with st.form("login_form"):
            st.markdown('<span class="input-label">USERNAME</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="admin")
            
            st.markdown('<span class="input-label">PASSWORD</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            submit = st.form_submit_button("Authenticate")
            
            if submit:
                if username == "admin" and password == "crypto123":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE ----------------
def dashboard_page():
    # Header
    head_col1, head_col2 = st.columns([5, 1])
    with head_col1:
        st.markdown("<h1 style='color:#4cc9f0; text-transform:uppercase;'>☁️ Volatility Dashboard</h1>", unsafe_allow_html=True)
    with head_col2:
        if st.sidebar.button("LOGOUT"):
            st.session_state['logged_in'] = False
            st.rerun()

    # (Insert your full Dashboard logic here - Table, Charts, etc.)
    st.info("You are now viewing the secure Risk Analyzer dashboard.")

# ---------------- APP LOGIC ----------------
if st.session_state['logged_in']:
    dashboard_page()
else:
    login_page()
