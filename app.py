import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- CSS: 100% WIDTH HEADER & CENTERED CARD ---
st.markdown("""
<style>
    /* 1. Global Deep Navy Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. THE TOP BAR (100% WIDTH) */
    /* Target the Streamlit header to make it full width and shift to top */
    [data-testid="stHeader"] {
        background-color: #1b4965 !important; /* Project Navy Blue */
        width: 100% !important;
        left: 0 !important;
        right: 0 !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: white !important;
        border-bottom: 2px solid #4cc9f0; /* Cyan accent line */
    }
    
    /* Remove padding that Streamlit adds to the main page container */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    /* 3. THE CENTERED LOGIN CARD */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 85vh; /* Centers card vertically below the header */
        width: 100%;
    }

    .login-card {
        background-color: #ffffff; 
        padding: 40px 45px;
        border-radius: 8px;
        width: 100%;
        max-width: 420px; /* Kept compact as requested */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    }

    .login-heading {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 25px;
        display: block;
        text-align: center;
    }

    .field-label {
        color: #333333;
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 6px;
    }

    /* Form and Button Styling */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dddddd !important;
        height: 42px !important;
    }

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
</style>
""", unsafe_allow_html=True)

# --- INJECT TEXT INTO THE FULL-WIDTH HEADER ---
# Since Streamlit's header is usually empty, we inject text via CSS/HTML
st.markdown("""
    <script>
        var header = window.parent.document.querySelector('header');
        header.innerHTML = '<div style="color:white; font-weight:bold; font-family:sans-serif; letter-spacing:2px;">CRYPTO RISK ANALYZER SYSTEM</div>';
    </script>
    """, unsafe_allow_html=True)

# --- LOGIN UI ---
def show_login():
    # Wrapper to center the card vertically and horizontally
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Nested container to hold the card
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<span class="login-heading">Login</span>', unsafe_allow_html=True)
        
        with st.form("auth_form"):
            st.markdown('<span class="field-label">Username:</span>', unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter username")
            
            st.markdown('<span class="field-label">Password:</span>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
            
            st.checkbox("Show Password")
            
            submit = st.form_submit_button("SIGN IN")
            
            if submit:
                # Synthesized credentials based on development preferences
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # Ensure dashboard.py exists in your folder with a main() function
    import dashboard
    dashboard.main()
