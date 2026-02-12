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

# ---------------- THE "HARD-FIX" CSS ----------------
st.markdown("""
<style>
/* 1. TOP NAVBAR FIX */
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

/* 2. REMOVE BLANK BOXES */
header, [data-testid="stHeader"], .st-emotion-cache-18ni7ve {
    display: none !important;
}

.block-container {
    padding-top: 0rem !important;
    margin-top: -20px !important;
}

/* 3. Global Background */
.stApp {
    background-color: #0d1b2a !important;
}

/* 4. THE THIN LOGIN CARD */
.login-card {
    background: transparent;
    width: 100%;
    max-width: 400px; 
    margin: 60px auto; 
}

/* 5. CENTERED CYAN LOGIN HEADING */
.login-title {
    color: #4cc9f0 !important; 
    font-family: 'Inter', sans-serif;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 30px;
    text-transform: uppercase;
    text-align: center;
}

/* 6. Form Styling & Input Icons */
.field-label {
    color: #778da9;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    display: block;
    margin-bottom: 5px;
}

div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

input {
    background-color: #ffffff !important;
    color: #0d1b2a !important;
    border-radius: 8px !important;
    height: 48px !important;
    padding-left: 45px !important;
    border: 1px solid #ced4da !important;
}

/* Icon Injections */
[data-testid="stTextInput"]:has(input[placeholder*="username"]) input {
    background-image: url('https://img.icons8.com/material-rounded/24/0d1b2a/user.png');
    background-repeat: no-repeat;
    background-position: 12px center;
}

[data-testid="stTextInput"]:has(input[type="password"]) input {
    background-image: url('https://img.icons8.com/material-rounded/24/0d1b2a/lock.png');
    background-repeat: no-repeat;
    background-position: 12px center;
}

/* 7. THE FIX: CENTERED CYAN LOGIN BUTTON */
/* Target the specific container that Streamlit uses for form buttons */
div.stFormSubmitButton {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: 30px !important; /* Space it down */
}

div.stFormSubmitButton > button {
    background-color: #4cc9f0 !important; /* Forces Cyan Color */
    color: #0d1b2a !important; /* Dark text for contrast */
    font-weight: 800 !important;
    width: 160px !important; 
    border-radius: 6px !important;
    border: none !important;
    text-transform: uppercase;
    padding: 12px !important;
    transition: 0.3s;
}

div.stFormSubmitButton > button:hover {
    background-color: #ffffff !important;
    box-shadow: 0px 0px 20px rgba(76, 201, 240, 0.6);
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR CONTENT ----------------
st.markdown("""
    <div style="position: fixed; top: 18px; left: 20px; z-index: 10000; color: white; font-weight: 800; font-family: sans-serif; font-size: 20px; letter-spacing: 1px;">
        CRYPTO RISK ANALYZER
    </div>
""", unsafe_allow_html=True)

# ---------------- LOGIN UI ----------------
def show_login():
    _, col_mid, _ = st.columns([1, 1.5, 1])

    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">LOGIN</div>', unsafe_allow_html=True)

        with st.form("auth_form"):
            st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
            username = st.text_input("user", label_visibility="collapsed", placeholder="Enter username")

            st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
            password = st.text_input("pass", type="password", label_visibility="collapsed", placeholder="••••••••")

            # The button is automatically placed in the center via the CSS above
            submit = st.form_submit_button("LOGIN")
            
            if submit:
                # Based on your interest in software development and Python
                if username == "admin" and password == "crypto123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- APP FLOW ----------------
if not st.session_state.authenticated:
    show_login()
else:
    # This calls the main logic for your cryptocurrency project
    import dashboard
    dashboard.main()
