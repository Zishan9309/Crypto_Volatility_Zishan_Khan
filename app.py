import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Risk Analyzer - Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* ===== REMOVE STREAMLIT HEADER COMPLETELY ===== */
header {visibility: hidden;}
[data-testid="stHeader"] {display: none;}
[data-testid="stToolbar"] {display: none;}
.stDecoration {display: none;}
.block-container {padding-top: 0rem;}

/* ===== FULL PAGE BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #0d1b2a, #1b4965);
}

/* ===== CENTER CONTENT VERTICALLY ===== */
.main-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ===== GLASS LOGIN CARD ===== */
.login-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    padding: 50px;
    border-radius: 16px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.15);
}

/* ===== TITLE ===== */
.login-title {
    text-align: center;
    color: #ffffff;
    font-size: 30px;
    font-weight: 600;
    margin-bottom: 35px;
}

/* ===== LABELS ===== */
.field-label {
    color: #e0e1dd;
    font-size: 14px;
    margin-bottom: 6px;
    display: block;
}

/* ===== INPUT FIELDS ===== */
input {
    background-color: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    height: 45px !important;
    border-radius: 8px !important;
}

/* ===== BUTTON ===== */
div.stButton > button {
    background: linear-gradient(90deg, #4cc9f0, #4361ee);
    color: white;
    font-weight: 600;
    width: 100%;
    border-radius: 8px;
    padding: 12px;
    margin-top: 20px;
    border: none;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #4361ee, #4cc9f0);
}

/* ===== FOOTER TEXT ===== */
.footer-text {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN FUNCTION ----------------
def show_login():

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Secure Login</div>', unsafe_allow_html=True)

    with st.form("login_form"):

        st.markdown('<span class="field-label">Username</span>', unsafe_allow_html=True)
        username = st.text_input("Username", label_visibility="collapsed")

        st.markdown('<span class="field-label">Password</span>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", label_visibility="collapsed")

        login_button = st.form_submit_button("SIGN IN")

        if login_button:
            if username == "admin" and password == "crypto123":
                st.session_state.authenticated = True
                st.success("Login Successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    st.markdown('<div class="footer-text">Crypto Risk Analyzer © 2026</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    import dashboard
    dashboard.main()
