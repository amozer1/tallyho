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

total_overdue = len(df[df["AgeDays"] > 7])

# =========================
# % FUNCTION
# =========================
def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# TOP HEADER (TITLE + SUBTITLE + DATE)
# =========================
left, middle, right = st.columns([2, 3, 1])

with left:
    st.markdown("""
    <h2 style="margin:0;color:white;">
        TQ & RFI Dashboard
    </h2>
    """, unsafe_allow_html=True)

with middle:
    st.markdown("""
    <p style="margin:10px 0 0 0;color:#9fb3c8;font-size:14px;">
        Project Overview and Response Analytics
    </p>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="text-align:right;">
        <h4 style="color:white;margin:0;">
            {datetime.today().strftime('%d %b %Y')}
        </h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECTION HEADER
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">
Project Overview Analytics
</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI STRIP
# =========================
k1, k2, k3 = st.columns(3)

with k1:
    st.metric("TQ Not Responded", len(tq_over), f"{pct(tq_over)}%")

with k2:
    st.metric("RFI Not Responded", len(rfi_over), f"{pct(rfi_over)}%")

with k3:
    st.metric("Total Outstanding >7 Days", total_overdue)

# =========================
# TOTAL BADGE
# =========================
st.markdown(f"""
<div style="
    text-align:center;
    margin-top:10px;
    margin-bottom:10px;
    color:white;
    font-size:16px;
">
    Total Overdue Items (>7 Days): <b>{total_overdue}</b>
</div>
""", unsafe_allow_html=True)

# =========================
# HEATMAP STYLE DONUT CHART
# =========================
tq_val = len(tq_over)
rfi_val = len(rfi_over)

labels = ["TQ Not Responded", "RFI Not Responded"]
values = [tq_val, rfi_val]

# heatmap-style colors (blue → red severity scale)
colors = ["#2F80ED", "#EB5757"]

fig = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.72,
            marker=dict(colors=colors),
            textinfo="label+value+percent",
            hoverinfo="label+value"
        )
    ]
)

fig.update_layout(
    title="TQ vs RFI Not Responded (>7 Days)",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    margin=dict(t=40, b=10, l=10, r=10),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)