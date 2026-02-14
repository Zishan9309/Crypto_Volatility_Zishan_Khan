import streamlit as st
import json
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Risk Analyzer - Auth",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- USER STORAGE LOGIC (Milestone 1) ----------------
USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    with open(USER_DB, "w") as f:
        json.dump(users, f)
    return True

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # Default mode

# ---------------- AUTH UI STYLING ----------------
st.markdown("""
<style>
/* 1. TOP NAVBAR */
[data-testid="stHeader"] {
    background-color: #0d1b2a !important;
    height: 60px !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    border-bottom: 2px solid #4cc9f0 !important;
    z-index: 9999 !important;
}
header, [data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 0rem !important; margin-top: -20px !important; }

/* 2. CARD & TITLES */
.stApp { background-color: #0d1b2a !important; }
.auth-card { background: transparent; width: 100%; max-width: 400px; margin: 60px auto; }
.auth-title {
    color: #4cc9f0 !important; 
    font-size: 34px; font-weight: 700;
    text-transform: uppercase; text-align: center; margin-bottom: 30px;
}
.field-label { color: #778da9; font-size: 13px; font-weight: 600; margin-bottom: 5px; display: block; }

/* 3. INPUTS & BUTTONS */
input { background-color: #ffffff !important; color: #0d1b2a !important; border-radius: 8px !important; height: 48px !important; }
div.stButton > button {
    background-color: #4cc9f0 !important; color: #0d1b2a !important;
    font-weight: 800 !important; width: 100% !important;
    border-radius: 6px !important; border: none !important;
    text-transform: uppercase; padding: 12px !important; margin-top: 20px;
}
.toggle-text { color: #778da9; text-align: center; margin-top: 15px; cursor: pointer; font-size: 14px; }
.toggle-link { color: #4cc9f0; font-weight: 700; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown('<div style="position: fixed; top: 18px; left: 20px; z-index: 10000; color: white; font-weight: 800; font-size: 20px;">CRYPTO RISK ANALYZER</div>', unsafe_allow_html=True)

# ---------------- AUTHENTICATION PAGES ----------------
def show_auth():
    _, col_mid, _ = st.columns([1, 1.5, 1])
    
    with col_mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="auth-title">SIGN IN</div>', unsafe_allow_html=True)
            with st.form("login_form"):
                st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
                user = st.text_input("user", label_visibility="collapsed")
                st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
                pwd = st.text_input("pass", type="password", label_visibility="collapsed")
                if st.form_submit_button("LOGIN"):
                    users = load_users()
                    if user in users and users[user] == pwd:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            
            # Link to Register
            st.markdown('<div class="toggle-text">New here? </div>', unsafe_allow_html=True)
            if st.button("Create an Account"):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            st.markdown('<div class="auth-title">REGISTER</div>', unsafe_allow_html=True)
            with st.form("reg_form"):
                st.markdown('<span class="field-label">CHOOSE USERNAME</span>', unsafe_allow_html=True)
                new_user = st.text_input("new_user", label_visibility="collapsed")
                st.markdown('<span class="field-label">CHOOSE PASSWORD</span>', unsafe_allow_html=True)
                new_pwd = st.text_input("new_pass", type="password", label_visibility="collapsed")
                if st.form_submit_button("REGISTER NOW"):
                    if new_user and new_pwd:
                        if save_user(new_user, new_pwd):
                            st.success("Registration Successful! Please Login.")
                            st.session_state.auth_mode = "login"
                            st.rerun()
                        else:
                            st.error("Username already exists.")
                    else:
                        st.warning("Please fill all fields.")

            # Link to Login
            st.markdown('<div class="toggle-text">Already have an account? </div>', unsafe_allow_html=True)
            if st.button("Back to Login"):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FLOW CONTROL ----------------
if not st.session_state.authenticated:
    show_auth()
else:
    import dashboard
    dashboard.main()
