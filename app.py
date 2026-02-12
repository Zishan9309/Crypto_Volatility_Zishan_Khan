import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crypto Risk Analyzer - Secure Login", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- THE HARD-RESET CSS ---
# This targets the specific Streamlit containers that create the "blank box" space.
st.markdown("""
<style>
    /* 1. Global Background (Matches Dashboard Navy) */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. REMOVE TOP BLANK SPACE COMPLETELY */
    /* Target the header bar and collapse it */
    header, [data-testid="stHeader"] { 
        display: none !important;
        height: 0 !important;
    }
    
    /* Force the main container to start at pixel 0 */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

    /* 3. THE CENTERED LOGIN CARD */
    .login-card {
        background-color: #ffffff; 
        padding: 40px 50px;
        border-radius: 10px;
        width: 100%;
        max-width: 420px;
        margin: 60px auto; /* Controls distance from the absolute top */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 30px;
        font-weight: 500;
        margin-bottom: 30px;
        display: block;
    }

    /* 4. ALIGNED LABELS & INPUTS */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
    }

    /* Remove Streamlit default widget borders inside the card */
    div[data-testid="stForm"] { 
        border: none !important; 
        padding: 0 !important; 
    }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 45px !important;
        border-radius: 5px !important;
    }

    /* 5. AESTHETIC SIGN IN BUTTON */
    div.stButton > button {
        background-color: #1b4965 !important; 
        color: #ffffff !important;
        font-weight: 700 !important;
        width: 100%;
        border-radius: 5px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
        transition: 0.3s;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        background-color: #4cc9f0 !important; 
        color: #0d1b2a !important;
        box-shadow: 0px 0px 15px rgba(76, 201, 240, 0.4);
    }

    /* 6. FOOTER LINKS */
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

# --- LOGIN UI LOGIC ---
def show_login():
    # Columns create the horizontal centering
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        # The main card container
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form", clear_on_submit=False):
            # Username Field
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username")
            
            st.write("") # Small gap
            
            # Password Field
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            # Show Password Checkbox (Standard UI)
            st.checkbox("Show Password")
            
            # Submit Action
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Based on your previous setup (admin/crypto123)
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        # Footer Links matching your reference image
        st.markdown("""
        <div class="footer-links">
            Forgot <a href="#">Username / Password</a>?<br>
            Don't have an account? <a href="#">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

# --- APP NAVIGATION ---
if not st.session_state['authenticated']:
    show_login()
else:
    # This calls your dashboard script
    import dashboard
    dashboard.main()
