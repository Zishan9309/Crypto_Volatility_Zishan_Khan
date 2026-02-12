import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crypto Risk Analyzer - Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: ABSOLUTE RESET TO REMOVE BLANK RECTANGLE ---
st.markdown("""
<style>
    /* 1. Global Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. REMOVE BLANK RECTANGLE (Streamlit Header) */
    /* This completely hides the top bar and its container */
    header, [data-testid="stHeader"], .st-emotion-cache-18ni7ve {
        display: none !important;
        height: 0 !important;
    }

    /* This removes the default 6rem padding at the top of the main container */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

    /* Removes internal vertical gap between the top and the first element */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }

    /* 3. CENTERED LOGIN CARD */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh; /* Centers the card vertically on the screen */
    }

    .login-card {
        background-color: #ffffff; 
        padding: 45px 50px;
        border-radius: 10px;
        width: 100%;
        max-width: 400px; /* Aesthetic compact width */
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    .login-heading {
        color: #1b4965;
        font-family: 'Inter', sans-serif;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 30px;
        display: block;
    }

    /* 4. LABELS & INPUTS */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
    }

    div[data-testid="stForm"] { 
        border: none !important; 
        padding: 0 !important; 
    }
    
    input {
        background-color: #f8f9fa !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 45px !important;
        border-radius: 5px !important;
    }

    /* 5. AESTHETIC SIGN IN BUTTON */
    div.stButton > button {
        background: linear-gradient(135deg, #1b4965 0%, #4cc9f0 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        width: 100%;
        border-radius: 5px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
        transition: 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(76, 201, 240, 0.4);
        filter: brightness(1.1);
    }

    .footer-links {
        margin-top: 25px;
        font-size: 13px;
        color: #666666;
    }
    .footer-links a {
        color: #1b4965;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN UI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def show_login():
    # Wrapper to control positioning
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Using a container to center the card horizontally
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            # Username Input
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("User", label_visibility="collapsed", placeholder="Enter username")
            
            st.write("") 
            
            # Password Input
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            st.checkbox("Show Password")
            
            # Action Button
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Use your credentials (admin / crypto123)
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        # Links at bottom
        st.markdown("""
        <div class="footer-links">
            Forgot <a href="#">Username / Password</a>?<br>
            Don't have an account? <a href="#">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FLOW CONTROL ---
if not st.session_state['authenticated']:
    show_login()
else:
    import dashboard
    dashboard.main()
