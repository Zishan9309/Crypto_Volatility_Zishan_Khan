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

/* Remove Streamlit Header Completely */
header {display: none !important;}
[data-testid="stHeader"] {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
.stDecoration {display: none !important;}

/* Remove Default Padding */
.block-container {
    padding: 0 !important;
    margin: 0 !important;
}

/* Full Page Background */
.stApp {
    background: linear-gradient(135deg, #0d1b2a, #1b4965);
}

/* Force Full Height Layout */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
}

/* Center Container */
.login-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Glass Card */
.login-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    padding: 50px;
    border-radius: 16px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.15);
}

/* Title */
.login-title {
    text-align: center;
    color: #ffffff;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 30px;
}

/* Labels */
.field-label {
    color: #e0e1dd;
    font-size: 14px;
    margin-bottom: 6px;
    display: block;
}

/* Inputs */
input {
    background-color: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    height: 45px !important;
    border-radius: 8px !important;
}

/* Button */
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
    transform: scale(1.04);
    background: linear-gradient(90deg, #4361ee, #4cc9f0);
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN FUNCTION ----------------
def show_login():

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Secure Login</div>', unsafe_allow_html=True)

    with st.form("login_form"):

        st.markdown('<span class="field-label">Username</span>', unsafe_allow_html=True)
        username = st.text_input("", label_visibility="collapsed")

        st.markdown('<span class="field-label">Password</span>', unsafe_allow_html=True)
        password = st.text_input("", type="password", label_visibility="collapsed")

        login_btn = st.form_submit_button("SIGN IN")

        if login_btn:
            if username == "admin" and password == "crypto123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    import dashboard
    dashboard.main()
