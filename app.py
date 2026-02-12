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


# ---------------- THE "THIN CARD" CSS ----------------
st.markdown("""
<style>
/* 1. Remove Streamlit Header & Blank Space */
header, [data-testid="stHeader"], [data-testid="stToolbar"] {
    display: none !important;
}

/* Remove default top padding to shift content up */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* 2. Global Background (Deep Navy) */
.stApp {
    background-color: #0d1b2a !important;
}

/* 3. Centered Thin Card Aesthetic */
.login-card {
    background: #ffffff;
    padding: 40px 30px;
    border-radius: 8px;
    width: 100%;
    max-width: 320px; /* Made the box very thin as requested */
    margin: 80px auto; 
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    text-align: center;
}

/* 4. Cyan Heading */
.login-title {
    color: #4cc9f0; /* Specific Cyan color */
    font-family: 'Inter', sans-serif;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 30px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 5. Labels & Inputs */
.field-label {
    color: #333333;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    display: block;
    margin-bottom: 6px;
}

div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

input {
    background-color: #f8f9fa !important;
    color: #0d1b2a !important;
    border: 1px solid #dee2e6 !important;
    height: 40px !important;
    border-radius: 4px !important;
    margin-bottom: 10px;
}

/* 6. Action Button */
div.stButton > button {
    background-color: #1b4965 !important;
    color: white !important;
    font-weight: 700 !important;
    width: 100%;
    border-radius: 4px !important;
    padding: 10px !important;
    margin-top: 10px;
    border: none !important;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #4cc9f0 !important; /* Glow Cyan on hover */
    color: #0d1b2a !important;
    box-shadow: 0px 0px 15px rgba(76, 201, 240, 0.4);
}

.footer-links {
    margin-top: 20px;
    font-size: 11px;
    color: #778da9;
}
.footer-links a { color: #1b4965; text-decoration: none; font-weight: bold;}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN LOGIC ----------------
def show_login():
    # Use center column for horizontal alignment
    _, col_mid, _ = st.columns([1, 0.8, 1])

    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)

        with st.form("auth_form", clear_on_submit=False):
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("User", label_visibility="collapsed", placeholder="Enter username")

            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="Enter password")

            # Standard checkbox
            st.checkbox("Show Password", key="show_pwd")

            if st.form_submit_button("SIGN IN"):
                if username == "admin" and password == "crypto123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Access Denied")

        st.markdown("""
        <div class="footer-links">
            Forgot <a href="#">Username / Password</a>?<br>
            Don't have an account? <a href="#">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------
if not st.session_state.authenticated:
    show_login()
else:
    # Ensure dashboard.py exists in the same folder
    import dashboard
    dashboard.main()
