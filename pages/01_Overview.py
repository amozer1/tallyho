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
# DATE + AGE CALCULATION
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

today = pd.Timestamp.today().normalize()
df["AgeDays"] = (today - df["Date Sent"]).dt.days

# =========================
# OVERDUE FILTER (>7 DAYS)
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

# =========================
# BOTH RISK LOGIC
# =========================
tq_recipients = set(tq_over["Recipient"])
rfi_recipients = set(rfi_over["Recipient"])

both_recipients = tq_recipients.intersection(rfi_recipients)

both_risk = df[
    (df["Recipient"].isin(both_recipients)) &
    (df["AgeDays"] > 7)
]

# =========================
# TOTAL OVERDUE
# =========================
total_overdue = len(df[df["AgeDays"] > 7])

def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# HEADER
# =========================
left, right = st.columns([3, 1])

with left:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:18px;
        border-radius:14px;
        border:1px solid rgba(0,191,255,0.25);
    ">
        <h2 style="color:white;margin:0;">
            📊 TQ & RFI ML Dashboard
        </h2>
        <p style="color:#9fb3c8;margin:5px 0 0 0;">
            Project Overview and Response Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="
        background:#0b1a2f;
        padding:18px;
        border-radius:14px;
        text-align:center;
        border:1px solid rgba(0,191,255,0.25);
    ">
        <h4 style="color:white;margin:0;">
            📅 {datetime.today().strftime('%d %b %Y')}
        </h4>
        <p style="color:#9fb3c8;margin-top:5px;">
            Download Report ⬇
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECTION TITLE
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">A - Project Overview Analytics</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# DONUT CHART (SEGMENTED CIRCLE)
# =========================

labels = ["TQ Overdue", "RFI Overdue", "Both Risk", "Other / Healthy"]
values = [
    len(tq_over),
    len(rfi_over),
    len(both_risk),
    max(total_overdue - (len(tq_over) + len(rfi_over)), 0)
]

colors = ["#00bfff", "#ff6bd6", "#00ffd5", "#1b2b3a"]

fig = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.65,
            marker=dict(colors=colors),
            textinfo="label+percent",
            hoverinfo="label+value"
        )
    ]
)

fig.update_layout(
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    margin=dict(t=30, b=10, l=10, r=10),
    showlegend=True,
    title="Overdue Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# KPI STRIP
# =========================
st.markdown("---")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Overdue", len(tq_over))

with k2:
    st.metric("RFI Overdue", len(rfi_over))

with k3:
    st.metric("High Risk Recipients", len(both_recipients))

with k4:
    st.metric("Total Overdue", total_overdue)