import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- AESTHETIC CSS FOR CENTERED LOGIN ---
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* Standardized Login Card in the Middle */
    .login-box {
        background-color: #1b263b;
        padding: 40px;
        border-radius: 12px;
        border: 2px solid #4cc9f0;
        width: 100%;
        max-width: 380px; /* Reduced width for a standard look */
        margin: 100px auto; /* Perfectly centered with top margin */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5), 0px 0px 15px rgba(76, 201, 240, 0.2);
        text-align: center;
    }

    .login-heading {
        color: #4cc9f0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Left-Aligned Labels for Inputs */
    .field-label {
        color: #778da9;
        font-size: 11px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 6px;
        letter-spacing: 1px;
    }

    /* Input Box Customization */
    input {
        background-color: #0d1b2a !important;
        color: white !important;
        border: 1px solid #415a77 !important;
        border-radius: 5px !important;
    }

    /* Centered Login Button */
    div.stButton > button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef) !important;
        color: #0d1b2a !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 6px !important;
        padding: 10px !important;
        margin-top: 15px;
        text-transform: uppercase;
    }

    div.stButton > button:hover {
        box-shadow: 0px 0px 15px #4cc9f0;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN UI ---
def show_login():
    # We use empty columns to force the 'login-box' into the center
    _, col_mid, _ = st.columns([1, 1.5, 1])
    
    with col_mid:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-heading">Sign In</h2>', unsafe_allow_html=True)
        
        # USERNAME FIELD
        st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
        username = st.text_input("User", label_visibility="collapsed", placeholder="admin")
        
        st.write("") # Small spacer
        
        # PASSWORD FIELD
        st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
        password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        # AUTH BUTTON
        if st.button("Access System"):
            if username == "admin" and password == "crypto123":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
if not st.session_state['authenticated']:
    show_login()
else:
    import dashboard
    dashboard.main()
