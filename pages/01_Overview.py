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

df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
today = pd.Timestamp.today().normalize()
df["AgeDays"] = (today - df["Date Sent"]).dt.days

# =========================
# SPLIT DATA
# =========================
tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

def classify(data):
    open_items = data[(data["Status"].str.lower() == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"].str.lower() == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]
    return len(open_items), len(closed_items), len(outstanding_items)

tq_open, tq_closed, tq_out = classify(tq)
rfi_open, rfi_closed, rfi_out = classify(rfi)

today_date = datetime.today().strftime('%d %b %Y')

# =========================
# HEADER
# =========================
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #0b1a2f, #0f2747);
    padding: 18px;
    border-radius: 16px;
    display:flex;
    justify-content:space-between;
    align-items:center;
">
    <div>
        <div style="color:white;font-size:22px;font-weight:800;">
            📊 TQ & RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;">
            Project Overview & SLA Performance
        </div>
    </div>

    <div style="color:white;text-align:right;">
        📅 {today_date}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI STRIP
# =========================
k1, k2, k3, k4 = st.columns(4)

k1.metric("TQ Total", len(tq))
k2.metric("RFI Total", len(rfi))
k3.metric("Outstanding (>7d)", len(df[df["AgeDays"] > 7]))
k4.metric("Total Items", len(df))

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# 🔵 CIRCULAR LIFECYCLE (RESTORED PROPERLY)
# =========================
c1, c2 = st.columns(2)

with c1:
    fig_tq = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Outstanding"],
        values=[tq_open, tq_closed, tq_out],
        hole=0.65,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"])
    )])

    fig_tq.update_layout(
        title="TQ Lifecycle",
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        showlegend=True,
        annotations=[dict(text=f"TQ<br>{len(tq)}", x=0.5, y=0.5, font_size=16, showarrow=False)]
    )

    st.plotly_chart(fig_tq, use_container_width=True)

with c2:
    fig_rfi = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Outstanding"],
        values=[rfi_open, rfi_closed, rfi_out],
        hole=0.65,
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"])
    )])

    fig_rfi.update_layout(
        title="RFI Lifecycle",
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        showlegend=True,
        annotations=[dict(text=f"RFI<br>{len(rfi)}", x=0.5, y=0.5, font_size=16, showarrow=False)]
    )

    st.plotly_chart(fig_rfi, use_container_width=True)

# =========================
# ANALYTICS SECTION
# =========================
st.markdown("### 📊 Overview Analytics")

fig = go.Figure()

fig.add_trace(go.Bar(
    name="TQ",
    x=["Open", "Closed", "Outstanding"],
    y=[tq_open, tq_closed, tq_out],
    marker_color="#2F80ED"
))

fig.add_trace(go.Bar(
    name="RFI",
    x=["Open", "Closed", "Outstanding"],
    y=[rfi_open, rfi_closed, rfi_out],
    marker_color="#FF4B4B"
))

fig.update_layout(
    barmode="group",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    height=400
)

st.plotly_chart(fig, use_container_width=True)