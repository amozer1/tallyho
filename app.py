import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.stage3 import tq_rfi_overview  # ✅ UPDATED IMPORT


st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

# =========================
# UI FRAMEWORK
# =========================
render_sidebar()
render_header()

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")

df = load_data()

# =========================
# STAGE 3 MODULE (KPI ENGINE)
# =========================
tq_rfi_overview(df)  # ✅ UPDATED CALL