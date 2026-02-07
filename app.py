import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #35d3ff;
        text-align: center;
    }
    h3 {
        color: #ffffff;
    }
    .stDataFrame {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown("<h1>📊 Crypto Volatility & Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center;'>Simple Streamlit App – Online Data Display</h3>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------- DESCRIPTION ----------------
st.info(
    "This application reads data from an **online source** and displays it in a clean, interactive table format using Streamlit."
)

# ---------------- READ ONLINE DATA ----------------
url = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"
df = pd.read_csv(url)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 3])

with col1:
    st.success("📌 Dataset Info")
    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")
    st.write("**Source:** Online CSV")

with col2:
    st.success("📈 Data Table")
    st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.write("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>Developed using Streamlit | Infosys Springboard Project</p>",
    unsafe_allow_html=True
)
