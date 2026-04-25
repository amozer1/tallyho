import streamlit as st
from utils.data_loader import load_data
import plotly.express as px

df = load_data()

st.title("Analytics")

fig = px.bar(df["Recipient"].value_counts(), title="Workload by Recipient")
st.plotly_chart(fig, use_container_width=True)

fig2 = px.histogram(df, x="AgeDays", color="Doc Type")
st.plotly_chart(fig2, use_container_width=True)