import streamlit as st
import pandas as pd

st.title("Simple Streamlit Data Table")

url = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"
df = pd.read_csv(url)

st.write("Online data displayed in table format:")
st.dataframe(df)
