import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crypto Risk Analyzer - Secure Login", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- CSS: THE "ONE BOX" SOLUTION ---
st.markdown("""
<style>
    /* 1. Global Background */
    .stApp {
        background-color: #0d1b2a !important;
    }

    /* 2. Hide extra Streamlit elements that create empty space */
    header, [data-testid="stHeader"] { visibility: hidden; height: 0; }
    
    /* 3. The Main Login Div */
    .login-card {
        background-color: #1b263b;
        padding: 50px 40px;
        border-radius: 15px;
        border: 2px solid #4cc9f0; /* Aesthetic Cyan Border */
        width: 100%;
        max-width: 380px; 
        margin: 100px auto; /* Centering horizontally and pushing from top */
        box-shadow: 0px 0px 30px rgba(76, 201, 240, 0.2);
        text-align: center;
    }

    /* 4. Heading inside the box */
    .login-heading {
        color: #4cc9f0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 35px;
        display: block;
    }

    /* 5. Left-Aligned Labels */
    .field-label {
        color: #778da9;
        font-size: 11px;
        font-weight: 600;
        text-align: left;
        display: block;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    /* 6. Input Style Overrides */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    input {
        background-color: #0d1b2a !important;
        color: white !important;
        border: 1px solid #415a77 !important;
    }

    /* 7. Centered Button inside the box */
    div.stButton > button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef) !important;
        color: #0d1b2a !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-top: 20px;
        text-transform: uppercase;
        border: none !important;
    }
    
    div.stButton > button:hover {
        box-shadow: 0px 0px 20px #4cc9f0;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN FORM CONTENT ---
def show_login():
    # Use columns strictly to center the div on the page
    _, col_mid, _ = st.columns([1, 1.5, 1])
    
    with col_mid:
        # ALL contents are wrapped in this DIV
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown('<span class="login-heading">System Login</span>', unsafe_allow_html=True)
        
        # Wrapping in a form to keep button and inputs together
        with st.form("auth_form", clear_on_submit=False):
            
            st.markdown('<span class="field-label">USERNAME</span>', unsafe_allow_html=True)
            username = st.text_input("User", label_visibility="collapsed", placeholder="admin")
            
            st.write("") # Spacer
            
            st.markdown('<span class="field-label">PASSWORD</span>', unsafe_allow_html=True)
            password = st.text_input("Pass", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            submit = st.form_submit_button("Access Dashboard")
            
            if submit:
                if username == "admin" and password == "crypto123":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Login Credentials")
                    
        st.markdown('</div>', unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['authenticated']:
    show_login()
else:
    # Ensure you have a file named dashboard.py with a main() function
    try:
        import dashboard
        dashboard.main()
    except ImportError:
        st.success("Authenticated! (Please ensure dashboard.py is in the folder)")
        st.info("You can now paste your Dashboard code inside a main() function in dashboard.py")
