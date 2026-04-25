import streamlit as st
from utils.data_loader import load_data
from utils.metrics import compute_metrics

st.title("🧠 AI Insights Engine")

file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(file) if file else load_data("data/TQ_TH.xlsx")

m = compute_metrics(df)

st.warning(f"{m['overdue7']} items overdue >7 days")
st.info(f"Highest workload: {m['df']['Sender'].value_counts().idxmax()}")
st.error(f"{m['overdue30']} items critically overdue")