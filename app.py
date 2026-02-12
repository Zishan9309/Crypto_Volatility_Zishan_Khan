import streamlit as st
import subprocess

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- AESTHETIC CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0d1b2a !important; }
    
    /* Center the login container */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 100px;
    }

    .login-form-div {
        background-color: #1b263b;
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #4cc9f0;
        width: 400px;
        box-shadow: 0px 0px 25px rgba(76, 201, 240, 0.3);
        margin: auto;
    }

    .form-heading {
        color: #4cc9f0;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    .field-label {
        color: #778da9;
        display: block;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
        text-align: left;
    }

    /* Input Overrides */
    input {
        background-color: #0d1b2a !important;
        color: white !important;
        border: 1px solid #415a77 !important;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #4cc9f0 !important;
        color: #0d1b2a !important;
        font-weight: 800 !important;
        width: 100%;
        border-radius: 8px !important;
        padding: 10px !important;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN LOGIC ---
def show_login():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-form-div">', unsafe_allow_html=True)
        st.markdown('<h2 class="form-heading">System Login</h2>', unsafe_allow_html=True)
        
        st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
        user = st.text_input("user", label_visibility="collapsed", placeholder="Enter admin ID")
        
        st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
        pwd = st.text_input("pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        if st.button("AUTHENTICATE"):
            if user == "admin" and pwd == "crypto123":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # This imports your dashboard code and runs it
    import dashboard
    dashboard.main()
