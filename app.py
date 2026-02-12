import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Secure Access | Crypto Risk Analyzer", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- THE ULTIMATE AESTHETIC CSS ---
st.markdown("""
<style>
    /* 1. Global Background - Deep Navy with subtle gradient */
    .stApp {
        background: radial-gradient(circle, #0d1b2a 0%, #010811 100%) !important;
    }

    /* 2. REMOVE ALL BLANK BOXES / HEADERS */
    header, [data-testid="stHeader"] { 
        display: none !important;
    }
    .block-container {
        padding: 0rem !important;
    }
    
    /* 3. 100% WIDTH TOP BAR SHIFTED TO TOP */
    .top-bar {
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #4cc9f0, #1b4965, #4cc9f0);
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }

    /* 4. LOGIN WRAPPER - Full Screen Centering */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        width: 100%;
    }

    /* 5. THE LOGIN CARD - White Glossy Aesthetic */
    .login-card {
        background-color: #ffffff; 
        padding: 50px 45px;
        border-radius: 12px;
        width: 100%;
        max-width: 400px; /* Minimized width as requested */
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.4);
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .login-heading {
        color: #1b4965;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 30px;
        display: block;
        text-align: center;
    }

    /* 6. LABELS & INPUTS */
    .field-label {
        color: #333333;
        font-size: 14px;
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
        height: 45px !important;
        border-radius: 6px !important;
    }
    
    input:focus {
        border-color: #4cc9f0 !important;
        box-shadow: 0 0 8px rgba(76, 201, 240, 0.4) !important;
    }

    /* 7. INTERACTIVE SIGN IN BUTTON */
    div.stButton > button {
        background: linear-gradient(45deg, #1b4965, #4cc9f0) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        width: 100%;
        border-radius: 6px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 15px rgba(76, 201, 240, 0.4);
        filter: brightness(1.1);
    }

    /* 8. FOOTER LINKS */
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

# --- LOGIN UI ---
def show_login():
    # Top 100% width accent bar
    st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Using columns only for centering logic
    _, col_mid, _ = st.columns([1, 1.3, 1])
    
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter your username")
            
            st.write("") 
            
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter your password")
            
            st.checkbox("Show Password", key="show_pwd")
            
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Based on your interests in software development and Python
                if username == "admin" and password == "crypto123":
                    with st.spinner("Authenticating..."):
                        st.session_state['authenticated'] = True
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
    st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # This imports the main function from your dashboard.py file
    try:
        import dashboard
        dashboard.main()
    except Exception as e:
        st.success("Successfully Authenticated!")
        st.info("Please ensure 'dashboard.py' is in the same folder.")
