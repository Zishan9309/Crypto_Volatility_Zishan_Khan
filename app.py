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

# ---------------- SHARED CSS ----------------
st.markdown("""
<style>
    .stApp { background-color: #0d1b2a !important; }
    
    /* Login Container */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
    }
    
    .login-box {
        background-color: #1b263b;
        padding: 50px;
        border-radius: 20px;
        border: 2px solid #4cc9f0;
        width: 450px;
        box-shadow: 0 0 30px rgba(76, 201, 240, 0.3);
    }
    
    .cyan-title {
        color: #4cc9f0 !important;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Label Styling - Left Aligned */
    .input-label {
        color: #778da9;
        font-weight: 600;
        text-align: left;
        margin-bottom: 5px;
        font-size: 14px;
        display: block;
    }

    /* Customizing Streamlit Inputs */
    .stTextInput > div > div > input {
        background-color: #0d1b2a !important;
        color: white !important;
        border: 1px solid #415a77 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4cc9f0 !important;
        box-shadow: 0 0 10px rgba(76, 201, 240, 0.5) !important;
    }

    /* Centering the Login Button */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 25px;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef);
        color: #0d1b2a;
        font-weight: 900;
        padding: 12px 40px;
        border-radius: 50px;
        border: none;
        transition: 0.3s;
        text-transform: uppercase;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #4cc9f0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------
def login_page():
    # Centering the login box on the page
    _, col_mid, _ = st.columns([1, 1.5, 1])
    
    with col_mid:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1 class='cyan-title'>System Login</h1>", unsafe_allow_html=True)
        
        # Username Field
        st.markdown("<span class='input-label'>USERNAME</span>", unsafe_allow_html=True)
        user = st.text_input("", placeholder="Enter your ID", key="user_input", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Password Field
        st.markdown("<span class='input-label'>PASSWORD</span>", unsafe_allow_html=True)
        pwd = st.text_input("", placeholder="••••••••", type="password", key="pwd_input", label_visibility="collapsed")
        
        # Centered Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        if st.button("Access Dashboard"):
            if user == "admin" and pwd == "crypto123":
                st.session_state['logged_in'] = True
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE ----------------
def dashboard_page():
    # Sidebar Logout
    st.sidebar.markdown("<h2 class='cyan-title'>Control Panel</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    # (Previous Dashboard Logic with Table and Charts goes here)
    st.markdown("<h1 class='cyan-title'>☁️ Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
    
    # Simple placeholder to show it works
    st.info("Authenticated successfully. Milestone 1 Data Loading...")
    
    # RE-INSERT TABLE LOGIC FROM PREVIOUS STEPS HERE...
    # For brevity, I've kept the logic focused on the login design. 
    # You can paste the table/chart code here to finish the app.

# ---------------- MAIN ----------------
if st.session_state['logged_in']:
    dashboard_page()
else:
    login_page()
