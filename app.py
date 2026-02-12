import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Secure Access | Crypto Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: THE MODERN AESTHETIC ---
st.markdown("""
<style>
    /* 1. Global Background - Deep Navy */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. REMOVE BLANK HEADER BOX */
    header, [data-testid="stHeader"] { 
        display: none !important;
        height: 0 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }

    /* 3. CENTERED AESTHETIC CARD */
    .login-card {
        background: rgba(255, 255, 255, 0.95); /* High-contrast white card */
        padding: 50px 45px;
        border-radius: 12px;
        width: 100%;
        max-width: 400px; /* Minimized modern width */
        margin: 60px auto; 
        box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.4);
        text-align: center;
    }

    /* 4. MODERN TYPOGRAPHY */
    .login-heading {
        color: #1b4965;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 30px;
        display: block;
        text-align: center;
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

    /* 5. INPUT FIELD STYLING */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #f8f9fa !important;
        color: #0d1b2a !important;
        border: 1px solid #dee2e6 !important;
        height: 45px !important;
        border-radius: 6px !important;
        padding-left: 10px !important;
    }
    
    input:focus {
        border-color: #4cc9f0 !important;
        box-shadow: 0 0 10px rgba(76, 201, 240, 0.3) !important;
    }

    /* 6. INTERACTIVE SIGN IN BUTTON */
    div.stButton > button {
        background: linear-gradient(135deg, #1b4965 0%, #4cc9f0 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        width: 100%;
        border-radius: 6px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(76, 201, 240, 0.4);
        filter: brightness(1.1);
    }

    /* 7. FOOTER LINKS */
    .footer-links {
        margin-top: 25px;
        font-size: 13px;
        color: #6c757d;
        text-align: center;
    }
    .footer-links a {
        color: #1b4965;
        text-decoration: none;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def show_login():
    # Centering columns
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form", clear_on_submit=False):
            # Username Field
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter your username")
            
            st.write("") # Aesthetic spacing
            
            # Password Field
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter your password")
            
            # Interactive Checkbox
            st.checkbox("Show Password", key="show_pwd")
            
            # Gradient Button
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Using standard credentials from previous versions
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        # Bottom Navigation Links
        st.markdown("""
        <div class="footer-links">
            Forgot <a href="#">Username / Password</a>?<br>
            Don't have an account? <a href="#">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # This leads to your Milestone 1 Dashboard
    st.success("Successfully Authenticated!")
    if st.button("Enter Dashboard"):
        import dashboard
        dashboard.main()
