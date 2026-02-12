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


# ---------------- NAVBAR & THIN CARD CSS ----------------
st.markdown("""
<style>
/* 1. MAKE HEADER A TOPMOST NAVBAR */
[data-testid="stHeader"] {
    background-color: #1b4965 !important; /* Navy Blue Navbar */
    height: 60px !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 20px !important;
    border-bottom: 2px solid #4cc9f0 !important; /* Cyan accent line */
    z-index: 9999 !important;
}

/* 2. REMOVE BLANK SPACE BELOW NAVBAR */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* 3. Global Background */
.stApp {
    background-color: #0d1b2a !important;
}

/* 4. THE THIN LOGIN CARD */
.login-card {
    background: #ffffff;
    padding: 40px 30px;
    border-radius: 8px;
    width: 100%;
    max-width: 340px; /* Very thin width */
    margin: 120px auto; /* Margin pushes it down from the navbar */
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    text-align: center;
}

/* 5. Cyan Heading */
.login-title {
    color: #4cc9f0; 
    font-family: 'Inter', sans-serif;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 25px;
    text-transform: uppercase;
}

/* 6. Form Styling */
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
    height: 42px !important;
    border-radius: 4px !important;
}

/* 7. Action Button */
div.stButton > button {
    background-color: #4cc9f0 !important; /* Cyan Button */
    color: #0d1b2a !important;
    font-weight: 700 !important;
    width: 100%;
    border-radius: 4px !important;
    padding: 10px !important;
    margin-top: 15px;
    border: none !important;
}

div.stButton > button:hover {
    background-color: #1b4965 !important;
    color: white !important;
    box-shadow: 0px 0px 15px rgba(76, 201, 240, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR CONTENT ----------------
# We use a custom div to place text inside the full-width top bar area
st.markdown("""
    <div style="position: fixed; top: 15px; left: 20px; z-index: 10000; color: white; font-weight: bold; font-family: sans-serif; font-size: 18px; letter-spacing: 1px;">
        CRYPTO RISK ANALYZER
    </div>
""", unsafe_allow_html=True)

# ---------------- LOGIN LOGIC ----------------
def show_login():
    _, col_mid, _ = st.columns([1, 1, 1])

    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Sign In</div>', unsafe_allow_html=True)

        with st.form("auth_form", clear_on_submit=False):
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("User", label_visibility="collapsed", placeholder="Enter username")

            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="Enter password")

            if st.form_submit_button("LOGIN"):
                if username == "admin" and password == "crypto123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Access Denied")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    # This leads to your Dashboard page
    import dashboard
    dashboard.main()
