import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- CSS: THE EXACT STRUCTURED LOGIN FORM ---
st.markdown("""
<style>
    /* 1. Global Deep Navy Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. Hide Streamlit Header */
    header, [data-testid="stHeader"] { visibility: hidden; height: 0; }
    
    /* 3. The Main Login Card (Centered) */
    .login-card {
        background-color: #ffffff; /* White card as per screenshot */
        padding: 50px 60px;
        border-radius: 8px;
        width: 100%;
        max-width: 500px; 
        margin: 80px auto; 
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    /* 4. Heading (Dark Gray for standard look) */
    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 500;
        margin-bottom: 30px;
        display: block;
    }

    /* 5. Left-Aligned Labels (Dark Blue/Gray) */
    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
    }

    /* 6. Input Overrides (White background, light borders) */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 45px !important;
    }

    /* 7. The SIGN IN Button (Matching Dashboard Cyan) */
    div.stButton > button {
        background-color: #1b4965 !important; /* Your specific Dark Blue */
        color: #ffffff !important;
        font-weight: 600 !important;
        width: 100%;
        border-radius: 4px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        background-color: #4cc9f0 !important; /* Hover glows Cyan */
        color: #0d1b2a !important;
    }

    /* 8. Footer links */
    .footer-links {
        margin-top: 20px;
        font-size: 13px;
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
    _, col_mid, _ = st.columns([1, 1.8, 1])
    
    with col_mid:
        # Card Wrapper
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            # Email Field
            st.markdown('<span class="field-label">Email:</span>', unsafe_allow_html=True)
            email = st.text_input("Email", label_visibility="collapsed", placeholder="Enter email")
            
            st.write("") 
            
            # Password Field
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            # Checkbox Placeholder
            st.checkbox("Show Password")
            
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Using the admin credentials previously discussed
                if email == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Login Credentials")
        
        # Bottom Links
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
    # Runs the dashboard.py file
    import dashboard
    dashboard.main()
