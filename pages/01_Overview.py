import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from utils.data_loader import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()
df.columns = df.columns.str.strip()

# =========================
# DATE + AGE
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
today = pd.Timestamp.today().normalize()
df["AgeDays"] = (today - df["Date Sent"]).dt.days

# =========================
# SPLIT DATA
# =========================
tq_df = df[df["Doc Type"] == "TQ"]
rfi_df = df[df["Doc Type"] == "RFI"]

# =========================
# STATUS COUNTS (TQ)
# =========================
tq_open = len(tq_df[tq_df["Status"].str.lower() == "open"])
tq_closed = len(tq_df[tq_df["Status"].str.lower() == "closed"])
tq_overdue = len(tq_df[tq_df["AgeDays"] > 7])

# =========================
# STATUS COUNTS (RFI)
# =========================
rfi_open = len(rfi_df[rfi_df["Status"].str.lower() == "open"])
rfi_closed = len(rfi_df[rfi_df["Status"].str.lower() == "closed"])
rfi_overdue = len(rfi_df[rfi_df["AgeDays"] > 7])

# =========================
# HEADER
# =========================
l, m, r = st.columns([2, 3, 1])

with l:
    st.markdown("<h2 style='color:white;'>TQ & RFI Dashboard</h2>", unsafe_allow_html=True)

with m:
    st.markdown("<p style='color:#9fb3c8;'>Project Overview & Document Lifecycle</p>", unsafe_allow_html=True)

with r:
    st.markdown(f"<h4 style='text-align:right;color:white;'>{datetime.today().strftime('%d %b %Y')}</h4>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# TWO DONUT CHARTS SIDE BY SIDE
# =========================
c1, c2 = st.columns(2)

# =========================
# TQ DONUT
# =========================
with c1:
    st.markdown("### TQ Overview")

    fig_tq = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Overdue (>7d)"],
        values=[tq_open, tq_closed, tq_overdue],
        hole=0.65,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"]),
        textinfo="label+value"
    )])

    fig_tq.update_layout(
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        height=400
    )

    st.plotly_chart(fig_tq, use_container_width=True)

# =========================
# RFI DONUT
# =========================
with c2:
    st.markdown("### RFI Overview")

    fig_rfi = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Overdue (>7d)"],
        values=[rfi_open, rfi_closed, rfi_overdue],
        hole=0.65,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"]),
        textinfo="label+value"
    )])

    fig_rfi.update_layout(
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        height=400
    )

    st.plotly_chart(fig_rfi, use_container_width=True)