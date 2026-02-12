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

# ---------------- THE ULTIMATE CLEANUP CSS ----------------
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

/* 2. DELETE THE WHITE RECTANGLE & GHOST BOXES */
/* Target any empty markdown or container blocks and hide them */
.element-container:has(div[style*="background-color: rgb(255, 255, 255)"]), 
.stMarkdown:empty, 
div[data-testid="stVerticalBlock"] > div:empty {
    display: none !important;
}

/* Remove default padding from the main block */
.block-container {
    padding-top: 2rem !important; /* Minimal spacing below navbar */
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}

/* 3. Global Background */
.stApp {
    background-color: #0d1b2a !important;
}

/* 4. THE THIN LOGIN FORM */
.login-card {
    background: transparent; /* Changed to transparent to match your screenshot style */
    padding: 20px;
    width: 100%;
    max-width: 360px; 
    margin: 80px auto; /* Centers it horizontally and pushes down from navbar */
    text-align: left;
}

/* 5. Cyan SIGN IN Text */
.login-title {
    color: #4cc9f0; 
    font-family: 'Inter', sans-serif;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 40px;
    text-transform: uppercase;
}

/* 6. Form Styling */
.field-label {
    color: #778da9;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
    display: block;
}

/* Input Overrides */
input {
    background-color: #ffffff !important;
    color: #0d1b2a !important;
    border-radius: 6px !important;
    height: 45px !important;
}

/* LOGIN Button */
div.stButton > button {
    background-color: #ffffff !important;
    color: #0d1b2a !important;
    font-weight: 700 !important;
    width: 100px; /* Slim button as per your latest screenshot */
    border-radius: 4px !important;
    border: 1px solid #ced4da !important;
    text-transform: uppercase;
}

div.stButton > button:hover {
    background-color: #f8f9fa !important;
    border-color: #4cc9f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR CONTENT ----------------
st.markdown("""
    <div style="position: fixed; top: 18px; left: 20px; z-index: 10000; color: white; font-weight: 800; font-family: sans-serif; font-size: 20px;">
        CRYPTO RISK ANALYZER
    </div>
""", unsafe_allow_html=True)

# ---------------- LOGIN LOGIC ----------------
def show_login():
    # We use empty markdown to bypass Streamlit's default spacing behavior
    st.markdown(" ") 
    
    _, col_mid, _ = st.columns([1, 1, 1])

    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">SIGN IN</div>', unsafe_allow_html=True)

        # Standard form inputs
        st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
        username = st.text_input("User", label_visibility="collapsed", placeholder="Enter username")

        st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="Enter password")

        if st.button("LOGIN"):
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
    import dashboard
    dashboard.main()
