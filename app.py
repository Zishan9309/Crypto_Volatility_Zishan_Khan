import streamlit as st
import json
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Risk Analyzer - Auth",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- USER DATABASE (Milestone 1 Local Storage) ----------------
USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return {}

def save_user(name, username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"name": name, "password": password}
    with open(USER_DB, "w") as f:
        json.dump(users, f)
    return True

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

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

/* 2. BACKGROUND & CARD */
.stApp { background-color: #0d1b2a !important; }
.auth-card { background: transparent; width: 100%; max-width: 400px; margin: 60px auto; }

.auth-title {
    color: #4cc9f0 !important; 
    font-family: 'Inter', sans-serif;
    font-size: 34px; font-weight: 700;
    text-transform: uppercase; text-align: center; margin-bottom: 30px;
}

.field-label { color: #778da9; font-size: 13px; font-weight: 600; margin-bottom: 5px; display: block; }

/* 3. INPUTS & CYAN BUTTONS */
input { background-color: #ffffff !important; color: #0d1b2a !important; border-radius: 8px !important; height: 48px !important; }

div.stFormSubmitButton > button {
    background-color: #4cc9f0 !important; color: #0d1b2a !important;
    font-weight: 800 !important; width: 100% !important;
    border-radius: 6px !important; border: none !important;
    text-transform: uppercase; padding: 12px !important; margin-top: 20px;
}

/* 4. TOGGLE TEXT STYLING (Transparent Buttons as Links) */
.toggle-container {
    text-align: center;
    margin-top: 25px;
    color: #778da9;
    font-size: 14px;
}

/* Make the Streamlit button look like a text link */
div.stButton > button {
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #4cc9f0 !important;
    text-decoration: underline !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-transform: none !important;
    box-shadow: none !important;
    display: inline !important;
    width: auto !important;
}

div.stButton > button:hover {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown('<div style="position: fixed; top: 18px; left: 20px; z-index: 10000; color: white; font-weight: 800; font-size: 20px; letter-spacing: 1px;"></div>', unsafe_allow_html=True)

# ---------------- AUTH PAGES ----------------
def show_auth():
    _, col_mid, _ = st.columns([1, 1.5, 1])
    
    with col_mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="auth-title">SIGN IN</div>', unsafe_allow_html=True)
            with st.form("login_form"):
                st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
                user = st.text_input("user", label_visibility="collapsed", placeholder="Enter username")
                st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
                pwd = st.text_input("pass", type="password", label_visibility="collapsed", placeholder="••••••••")
                
                # Primary action button
                if st.form_submit_button("LOGIN"):
                    users = load_users()
                    if user in users and users[user]["password"] == pwd:
                        st.session_state.authenticated = True
                        st.session_state.current_user = users[user]["name"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            
            # Text link navigation
            st.write("Don't have an account?")
            if st.button("Register"):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            st.markdown('<div class="auth-title">REGISTER</div>', unsafe_allow_html=True)
            with st.form("reg_form"):
                st.markdown('<span class="field-label">NAME</span>', unsafe_allow_html=True)
                reg_name = st.text_input("reg_name", label_visibility="collapsed", placeholder="Full Name")
                st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
                reg_user = st.text_input("reg_user", label_visibility="collapsed", placeholder="Username")
                st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
                reg_pwd = st.text_input("reg_pass", type="password", label_visibility="collapsed", placeholder="Password")
                
                # Primary action button in Cyan
                if st.form_submit_button("REGISTER"):
                    if reg_name and reg_user and reg_pwd:
                        if save_user(reg_name, reg_user, reg_pwd):
                            st.success("Registration Successful!")
                            st.session_state.auth_mode = "login"
                            st.rerun()
                        else:
                            st.error("Username already exists.")
                    else:
                        st.warning("All fields required.")

            # Text link navigation
            st.write("Already have an account?")
            if st.button("Login"):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_auth()
else:
    import dashboard
    dashboard.main()
