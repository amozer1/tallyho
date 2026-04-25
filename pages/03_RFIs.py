import streamlit as st
from utils.data_loader import load_data

df = load_data()
df = df[df["Doc Type"]=="RFI"]

st.title("RFI Register")
st.dataframe(df, use_container_width=True)