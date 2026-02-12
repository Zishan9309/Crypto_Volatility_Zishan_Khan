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


# ---------------- CSS: AESTHETIC OVERHAUL ----------------
st.markdown("""
<style>
/* 1. Remove Streamlit Header and Blank Space */
header, [data-testid="stHeader"], [data-testid="stToolbar"] {
    display: none !important;
}

/* Hard reset for top padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* 2. Global Background (Deep Navy) */
.stApp {
    background: radial-gradient(circle, #1b4965 0%, #0d1b2a 100%) !important;
}

/* 3. Centered Flex Wrapper */
.main-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* 4. The Login Card (Clean White Aesthetic) */
.login-card {
    background: #ffffff;
    padding: 50px 45px;
    border-radius: 12px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.4);
    text-align: center;
    margin: 40px auto;
}

/* 5. Typography */
.login-title {
    color: #1b4965;
    font-family: 'Inter', sans-serif;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 30px;
}

.field-label {
    color: #333333;
    font-size: 14px;
    font-weight: 600;
    text-align: left;
    display: block;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

/* 6. Inputs Styling */
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

input {
    background-color: #f8f9fa !important;
    color: #0d1b2a !important;
    border: 1px solid #dee2e6 !important;
    height: 45px !important;
    border-radius: 6px !important;
}

input:focus {
    border-color: #4cc9f0 !important;
    box-shadow: 0 0 10px rgba(76, 201, 240, 0.3) !important;
}

/* 7. Button (Cyan Gradient) */
div.stButton > button {
    background: linear-gradient(135deg, #1b4965 0%, #4cc9f0 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    width: 100%;
    border-radius: 6px !important;
    padding: 12px !important;
    margin-top: 20px;
    border: none !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 8px 20px rgba(76, 201, 240, 0.4);
    filter: brightness(1.1);
}

/* 8. Footer Links */
.footer-links {
    margin-top: 25px;
    font-size: 13px;
    color: #6c757d;
}
.footer-links a {
    color: #1b4965;
    text-decoration: none;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN FUNCTION ----------------
def show_login():
    # Vertical spacer removed, handled by margin in CSS
    _, col_mid, _ = st.columns([1, 1.2, 1])

    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)

        # Using custom labels for better control
        st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
        username = st.text_input("User", label_visibility="collapsed", placeholder="Enter username")

        st.markdown('<br><span class="field-label">Password:</span>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="Enter password")

        st.checkbox("Show Password", key="show_pwd")

        if st.button("SIGN IN"):
            # Credentials support derived from development interests
            if username == "admin" and password == "crypto123":
                st.session_state.authenticated = True
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


# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    # This leads to the Cryptocurrency Dashboard
    import dashboard
    dashboard.main()
