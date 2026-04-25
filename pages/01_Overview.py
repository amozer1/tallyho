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
# SPLIT
# =========================
tq_df = df[df["Doc Type"] == "TQ"]
rfi_df = df[df["Doc Type"] == "RFI"]

# =========================
# CLASSIFICATION FUNCTION
# =========================
def classify(data):
    open_items = data[(data["Status"].str.lower() == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"].str.lower() == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]

    return len(open_items), len(closed_items), len(outstanding_items)

# =========================
# TQ VALUES
# =========================
tq_open, tq_closed, tq_outstanding = classify(tq_df)

# =========================
# RFI VALUES
# =========================
rfi_open, rfi_closed, rfi_outstanding = classify(rfi_df)

# =========================
# HEADER
# =========================
l, m, r = st.columns([2, 3, 1])

with l:
    st.markdown("<h2 style='color:white;'>TQ & RFI Dashboard</h2>", unsafe_allow_html=True)

with m:
    st.markdown("<p style='color:#9fb3c8;'>Project Overview & SLA Performance</p>", unsafe_allow_html=True)

with r:
    st.markdown(f"<h4 style='text-align:right;color:white;'>{datetime.today().strftime('%d %b %Y')}</h4>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# TWO DONUTS (FINAL MODEL)
# =========================
c1, c2 = st.columns(2)

# =========================
# TQ DONUT
# =========================
with c1:
    st.markdown("### TQ Lifecycle")

    fig_tq = go.Figure(data=[go.Pie(
        labels=["Open (≤7d)", "Closed", "Outstanding (>7d)"],
        values=[tq_open, tq_closed, tq_outstanding],
        hole=0.70,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"]),
        textinfo="label+percent",
        hoverinfo="label+value+percent"
    )])

    fig_tq.update_layout(
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        height=350
    )

    st.plotly_chart(fig_tq, use_container_width=True)

# =========================
# RFI DONUT
# =========================
with c2:
    st.markdown("### RFI Lifecycle")

    fig_rfi = go.Figure(data=[go.Pie(
        labels=["Open (≤7d)", "Closed", "Outstanding (>7d)"],
        values=[rfi_open, rfi_closed, rfi_outstanding],
        hole=0.70,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"]),
        textinfo="label+percent",
        hoverinfo="label+value+percent"
    )])

    fig_rfi.update_layout(
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        height=350
    )

    st.plotly_chart(fig_rfi, use_container_width=True)