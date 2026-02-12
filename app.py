import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- AESTHETIC CSS FOR LOGIN PAGE ---
st.markdown("""
<style>
    /* Global Deep Navy Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* Centering the Login Box */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 80px;
    }

    /* The Main Div (The Login Card) */
    .login-card {
        background-color: #1b263b;
        padding: 50px;
        border-radius: 15px;
        border: 2px solid #4cc9f0; /* Glowing Cyan Border */
        width: 450px; /* Medium Length */
        height: auto; /* Medium Height */
        box-shadow: 0px 0px 30px rgba(76, 201, 240, 0.25);
        margin: auto;
        text-align: center;
    }

    /* Heading inside the card */
    .login-heading {
        color: #4cc9f0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 35px;
    }

    /* Field Labels Aligned Left */
    .label-text {
        color: #778da9;
        font-size: 12px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    /* Login Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef) !important;
        color: #0d1b2a !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        margin-top: 20px;
        transition: 0.3s ease-in-out;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 20px #4cc9f0;
    }

    /* Hide Streamlit default UI elements on Login */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- LOGIN FORM UI ---
def show_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-heading">Login</h1>', unsafe_allow_html=True)
        
        # Username Input
        st.markdown('<span class="label-text">USERNAME</span>', unsafe_allow_html=True)
        username = st.text_input("user", label_visibility="collapsed", placeholder="Enter Username")
        
        st.write("") # Spacer
        
        # Password Input
        st.markdown('<span class="label-text">PASSWORD</span>', unsafe_allow_html=True)
        password = st.text_input("pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        # Login Button
        if st.button("SIGN IN"):
            if username == "admin" and password == "crypto123":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- APP NAVIGATION ---
if not st.session_state['authenticated']:
    show_login()
else:
    # This imports and executes the dashboard file
    import dashboard
    dashboard.main()
