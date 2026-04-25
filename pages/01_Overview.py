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
# CLASSIFICATION
# =========================
def classify(data):
    open_items = data[(data["Status"].str.lower() == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"].str.lower() == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]
    return len(open_items), len(closed_items), len(outstanding_items)

tq_open, tq_closed, tq_outstanding = classify(tq_df)
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
# DONUT FUNCTION (REUSABLE)
# =========================
def donut(title, open_v, closed_v, outstanding_v):
    fig = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Outstanding"],
        values=[open_v, closed_v, outstanding_v],
        hole=0.75,
        textinfo="label+value+percent",
        insidetextorientation="radial",
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"])
    )])

    fig.update_layout(
        title=title,
        paper_bgcolor="#0b1a2f",
        font=dict(color="white", size=12),
        height=360,
        margin=dict(t=40, b=20, l=10, r=10)
    )

    return fig

# =========================
# LAYOUT
# =========================
c1, c2 = st.columns(2)

with c1:
    st.markdown("### TQ Lifecycle")
    st.plotly_chart(donut("TQ", tq_open, tq_closed, tq_outstanding), use_container_width=True)

with c2:
    st.markdown("### RFI Lifecycle")
    st.plotly_chart(donut("RFI", rfi_open, rfi_closed, rfi_outstanding), use_container_width=True)