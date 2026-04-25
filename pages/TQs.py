import streamlit as st
from utils.data_loader import load_data

df = load_data()
df = df[df["Doc Type"]=="TQ"]

st.title("TQ Register")
st.dataframe(df, use_container_width=True)