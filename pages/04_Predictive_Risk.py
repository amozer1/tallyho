import streamlit as st
from utils.data_loader import load_data
from utils.ml_engine import train_model, predict

st.set_page_config(layout="wide")

file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(file) if file else load_data("data/TQ_TH.xlsx")

model, acc, df = train_model(df)

df = predict(model, df)

st.success(f"Model Accuracy: {round(acc*100,2)}%")

st.dataframe(
    df[[
        "Doc Type",
        "Seq No",
        "Sender",
        "Recipient",
        "AgeDays",
        "Risk %",
        "Risk Level"
    ]],
    use_container_width=True
)