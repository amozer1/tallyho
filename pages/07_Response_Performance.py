import streamlit as st
from utils.data_loader import load_data
import plotly.express as px

df = load_data()

fig = px.box(df, x="Recipient", y="ResponseDays")
st.plotly_chart(fig, use_container_width=True)