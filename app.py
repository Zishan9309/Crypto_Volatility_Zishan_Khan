import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- CSS: FIXED SPACING & COMPACT WIDTH ---
st.markdown("""
<style>
    /* 1. Global Deep Navy Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. REMOVE BLANK BOX: Hide Streamlit Header & Padding */
    header, [data-testid="stHeader"] { 
        visibility: hidden !important; 
        height: 0 !important; 
        padding: 0 !important;
    }
    .block-container {
        padding-top: 50px !important;
    }
    
    /* 3. The Main Login Card (Minimized Width) */
    .login-card {
        background-color: #ffffff; 
        padding: 40px 45px;
        border-radius: 8px;
        width: 100%;
        max-width: 420px; /* Slightly minimized width */
        margin: 0 auto; 
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    /* 4. Heading Style */
    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 25px;
        display: block;
    }

    /* 5. Left-Aligned Labels */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 6px;
    }

    /* 6. Input Styling */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 40px !important;
    }

    /* 7. SIGN IN Button (Project Color Palette) */
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

    .footer-links {
        margin-top: 20px;
        font-size: 12px;
        color: #666666;
    }
    .footer-links a {
        color: #1b4965;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN UI FUNCTION ---
def show_login():
    # Centering the card horizontally
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            # Username Field (Previously Email)
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username")
            
            st.write("") 
            
            # Password Field
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            # Show Password Checkbox
            st.checkbox("Show Password")
            
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Using the credentials from previous conversations
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        
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
    # This calls the main() function in your dashboard.py file
    import dashboard
    dashboard.main()
