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


# ---------------- CSS ----------------
st.markdown("""
<style>

/* Remove Streamlit header */
header {visibility: hidden;}
[data-testid="stHeader"] {display: none;}
[data-testid="stToolbar"] {display: none;}
.stDecoration {display: none;}

/* Remove top padding */
.block-container {
    padding-top: 2rem;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0d1b2a, #1b4965);
}

/* Login Card */
.login-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.5);
}

/* Title */
.login-title {
    text-align: center;
    color: white;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 25px;
}

/* Labels */
label {
    color: #e0e1dd !important;
    font-weight: 500 !important;
}

/* Inputs */
input {
    background-color: rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg, #4cc9f0, #4361ee);
    color: white;
    font-weight: 600;
    width: 100%;
    border-radius: 8px;
    padding: 10px;
    border: none;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #4361ee, #4cc9f0);
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN FUNCTION ----------------
def show_login():

    # Center using columns
    col1, col2, col3 = st.columns([2, 1.5, 2])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🔐 Secure Login</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("SIGN IN"):
            if username == "admin" and password == "crypto123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    import dashboard
    dashboard.main()
