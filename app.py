import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crypto Risk Analyzer - Secure Login",
    layout="wide"
)

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- CUSTOM CSS ---
st.markdown("""
<style>

    /* ===== GLOBAL BACKGROUND ===== */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* ===== REMOVE STREAMLIT HEADER / WHITE SPACE ===== */
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stToolbar {display: none !important;}
    .stDecoration {display: none !important;}

    .block-container {
        padding-top: 0rem !important;
    }

    /* ===== LOGIN CARD ===== */
    .login-card {
        background-color: #ffffff;
        padding: 40px 45px;
        border-radius: 8px;
        width: 100%;
        max-width: 400px;
        margin: 80px auto 0 auto;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* ===== HEADING ===== */
    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 25px;
        text-align: center;
    }

    /* ===== LABELS ===== */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 6px;
        display: block;
    }

    /* ===== INPUT FIELDS ===== */
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 42px !important;
    }

    /* ===== BUTTON ===== */
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

    /* ===== FOOTER ===== */
    .footer-links {
        margin-top: 20px;
        font-size: 12px;
        color: #666666;
        text-align: center;
    }

    .footer-links a {
        color: #1b4965;
        text-decoration: none;
    }

</style>
""", unsafe_allow_html=True)


# --- LOGIN FUNCTION ---
def show_login():

    _, col_center, _ = st.columns([1, 1.2, 1])

    with col_center:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-heading">Login</div>', unsafe_allow_html=True)

        with st.form("login_form"):

            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed")

            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed")

            submit = st.form_submit_button("SIGN IN")

            if submit:
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


# --- APP FLOW ---
if not st.session_state.authenticated:
    show_login()
else:
    import dashboard
    dashboard.main()
