import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.venn_overview import render_venn_overview


st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

# =========================
# GLOBAL UI (YOUR CODE)
# =========================
render_sidebar()
render_header()


# =========================
# LOAD DATA (REQUIRED)
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")


df = load_data()


# =========================
# VENN MODULE (YOUR DIAGRAM)
# =========================
render_venn_overview(df)