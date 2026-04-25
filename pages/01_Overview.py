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

def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# TOP HEADER (MAIN LAYOUT ROW)
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
# SECTION TITLE
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
# KPI STRIP (TOP CORNER STYLE)
# =========================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Not Responded", len(tq_over), f"{pct(tq_over)}%")

with k2:
    st.metric("RFI Not Responded", len(rfi_over), f"{pct(rfi_over)}%")

with k3:
    st.metric("Both Risk", len(both_risk), f"{pct(both_risk)}%")

with k4:
    st.metric("Total >7 Days", total_overdue)

# =========================
# DONUT CHART (MAIN VISUAL)
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
# SUMMARY CARDS
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