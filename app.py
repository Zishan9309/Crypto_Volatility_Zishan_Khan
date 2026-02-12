import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- THE ULTIMATE "ZERO GAP" CSS ---
st.markdown("""
<style>
    /* 1. Global Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. COMPLETELY REMOVE TOP HEADER & PADDING */
    /* This kills the header bar entirely */
    header, [data-testid="stHeader"] { 
        display: none !important;
    }
    
    /* This removes the massive default gap at the top of the page */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* This removes the internal vertical gap between elements */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    /* 3. The Login Wrapper (Used for absolute positioning) */
    .login-wrapper {
        display: flex;
        justify-content: center;
        padding-top: 40px; /* Adjust this to move the card up or down slightly */
        width: 100%;
    }

    /* 4. The Login Card (Your white div box) */
    .login-card {
        background-color: #ffffff; 
        padding: 40px 45px;
        border-radius: 8px;
        width: 100%;
        max-width: 400px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    }

    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 25px;
        display: block;
        text-align: center;
    }

    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 6px;
    }

    /* Streamlit Form Fixes */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 42px !important;
    }

    div.stButton > button {
        background-color: #1b4965 !important; 
        color: #ffffff !important;
        font-weight: 600 !important;
        width: 100%;
        border-radius: 4px !important;
        padding: 10px !important;
        margin-top: 15px;
        text-transform: uppercase;
        border: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #4cc9f0 !important; 
        color: #0d1b2a !important;
    }

    .footer-links {
        margin-top: 20px;
        font-size: 12px;
        color: #666666;
        text-align: center;
    }
    .footer-links a { color: #1b4965; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- LOGIN UI ---
def show_login():
    # Wrap in a custom div to bypass Streamlit's internal layout padding
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    container = st.container()
    with container:
        # Columns used only to maintain the width constraints
        _, col_mid, _ = st.columns([1, 1.2, 1])
        with col_mid:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
            
            with st.form("auth_form"):
                st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
                username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username")
                
                st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
                password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
                
                st.checkbox("Show Password")
                
                submit = st.form_submit_button("SIGN IN")
                
                if submit:
                    if username == "admin" and password == "crypto123":
                        st.session_state['authenticated'] = True
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password")
            
            st.markdown("""
            <div class="footer-links">
                Forgot <a href="#">Username / Password</a>?<br>
                Don't have an account? <a href="#">Sign up</a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # Ensure you have dashboard.py in your folder
    import dashboard
    dashboard.main()
