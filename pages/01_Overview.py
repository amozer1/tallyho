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
# OVERDUE (>7 DAYS)
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

total_overdue = len(df[df["AgeDays"] > 7])

# =========================
# BOTH RISK
# =========================
tq_recipients = set(tq_over["Recipient"])
rfi_recipients = set(rfi_over["Recipient"])

both_recipients = tq_recipients.intersection(rfi_recipients)

both_risk = df[
    (df["Recipient"].isin(both_recipients)) &
    (df["AgeDays"] > 7)
]

# =========================
# % FUNCTION
# =========================
def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# HEADER (MAIN TITLE)
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:18px;
    border-radius:14px;
    border:1px solid rgba(0,191,255,0.25);
">
    <h2 style="color:white;margin:0;">
        Not Responded Within 7 Days
    </h2>
    <p style="color:#9fb3c8;margin:5px 0 0 0;">
        TQ and RFI Ageing Overview
    </p>
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
# TOP RIGHT KPI PANEL (SMALL SQUARE STYLE)
# =========================
k1, k2, k3, k4 = st.columns([1.2, 1, 1, 1])

with k1:
    st.markdown("")

with k2:
    st.metric("TQ Not Responded", len(tq_over), f"{pct(tq_over)}%")

with k3:
    st.metric("RFI Not Responded", len(rfi_over), f"{pct(rfi_over)}%")

with k4:
    st.metric("Total >7 Days", total_overdue)

# =========================
# MAIN DONUT CHART (OVERVIEW)
# =========================

st.markdown("### TQ & RFI Ageing Overview")

labels = ["TQ Only", "RFI Only", "Both Risk", "Other"]
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
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# SMALL SUMMARY CARDS (BOTTOM INSIGHT ROW)
# =========================

st.markdown("### Summary Breakdown")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(f"TQ Not Responded\n\n**{len(tq_over)} ({pct(tq_over)}%)**")

with c2:
    st.info(f"RFI Not Responded\n\n**{len(rfi_over)} ({pct(rfi_over)}%)**")

with c3:
    st.info(f"Both Risk\n\n**{len(both_risk)} ({pct(both_risk)}%)**")

with c4:
    st.warning(f"Total Outstanding >7\n\n**{total_overdue} (100%)**")