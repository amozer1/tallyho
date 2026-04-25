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

# =========================
# TOTALS
# =========================
total_tq = len(tq)
total_rfi = len(rfi)
total_out = len(df[df["AgeDays"] > 7])

today_date = datetime.today().strftime('%d %b %Y')

# =========================
# HEADER
# =========================
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #0b1a2f, #0f2747);
    padding: 18px 22px;
    border-radius: 16px;
    border: 1px solid rgba(0,191,255,0.25);
    display:flex;
    justify-content:space-between;
    align-items:center;
">

    <div>
        <div style="color:white;font-size:22px;font-weight:800;">
            📊 TQ & RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;">
            Project Overview & SLA Performance Analytics
        </div>
    </div>

    <div style="text-align:right;">
        <div style="color:white;font-weight:600;">
            📅 {today_date}
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            Live Intelligence View
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI STRIP
# =========================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total TQs", total_tq)
k2.metric("Total RFIs", total_rfi)
k3.metric("Outstanding (>7 days)", total_out)
k4.metric("Total Items", len(df))

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# ANALYTICS SECTION TITLE
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:10px 14px;
    border-radius:10px;
    border:1px solid rgba(0,191,255,0.15);
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">A - Project Overview Analytics</h3>
<p style="color:#9fb3c8;margin:5px 0 0 0;">
TQ & RFI Lifecycle and SLA Performance Overview
</p>
</div>
""", unsafe_allow_html=True)

# =========================
# CHART 1: TQ vs RFI LIFECYCLE
# =========================
fig1 = go.Figure()

fig1.add_trace(go.Bar(
    name="TQ",
    x=["Open", "Closed", "Outstanding"],
    y=[tq_open, tq_closed, tq_out],
    marker_color="#2F80ED"
))

fig1.add_trace(go.Bar(
    name="RFI",
    x=["Open", "Closed", "Outstanding"],
    y=[rfi_open, rfi_closed, rfi_out],
    marker_color="#FF4B4B"
))

fig1.update_layout(
    barmode="group",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    height=400,
    title="TQ vs RFI Lifecycle Overview"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2: SIMPLE AGEING BREAKDOWN
# =========================
bins = [0, 7, 14, 30, 1000]
labels = ["0–7", "8–14", "15–30", "30+"]

df["AgeGroup"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

age_counts = df["AgeGroup"].value_counts().sort_index()

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=age_counts.index.astype(str),
    y=age_counts.values,
    marker_color="#00FFD5"
))

fig2.update_layout(
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    height=350,
    title="Ageing Breakdown (>7 Days Visibility)"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# SLA RISK INDICATOR (SIMPLE RULE-BASED)
# =========================
risk_score = round((total_out / len(df)) * 100, 1) if len(df) else 0

st.markdown("### ⚠ SLA Risk Snapshot")

st.markdown(f"""
<div style="
    background:#0b1a2f;
    padding:18px;
    border-radius:12px;
    border:1px solid rgba(255,75,75,0.2);
    text-align:center;
">
    <h2 style="color:#FF4B4B;margin:0;">
        Risk Score: {risk_score}%
    </h2>
    <p style="color:#9fb3c8;">
        Based on overdue workload (>7 days)
    </p>
</div>
""", unsafe_allow_html=True)
