import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- IMPROVED CSS: REMOVE TOP SPACE & SHIFT UP ---
st.markdown("""
<style>
    /* 1. Global Deep Navy Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. REMOVE BLANK BOX & PADDING: Forces content to the top */
    header, [data-testid="stHeader"] { 
        display: none !important; 
    }
    
    .block-container {
        padding-top: 1rem !important; /* Minimal gap at the very top */
        padding-bottom: 0rem !important;
    }

    /* 3. The Main Login Card (Shifted Up & Centered) */
    .login-card {
        background-color: #ffffff; /* White card for high contrast */
        padding: 40px 45px;
        border-radius: 8px;
        width: 100%;
        max-width: 400px; /* Compact width */
        margin: 40px auto; /* Reduced top margin to shift it up */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* 4. Login Heading (Centered) */
    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 25px;
        display: block;
        text-align: center;
    }

    /* 5. Field Labels (Left Aligned) */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 6px;
    }

    /* 6. Form/Input Overrides */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 42px !important;
        border-radius: 4px !important;
    }

    /* 7. Sign In Button (Aesthetic Cyan/Blue) */
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
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #4cc9f0 !important; 
        color: #0d1b2a !important;
        box-shadow: 0px 0px 15px rgba(76, 201, 240, 0.4);
    }

    .footer-links {
        margin-top: 20px;
        font-size: 12px;
        color: #666666;
        text-align: center;
    }
    .footer-links a { color: #1b4965; text-decoration: none; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- LOGIN UI ---
def show_login():
    # Using center column to keep the card centered horizontally
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        # All login elements inside the main white div
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username")
            
            st.write("") 
            
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            st.checkbox("Show Password")
            
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        # Adding those standard aesthetic links below the button
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
    # This calls your main dashboard content
    import dashboard
    dashboard.main()
