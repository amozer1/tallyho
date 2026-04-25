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
# FILTERS
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

total_overdue = len(df[df["AgeDays"] > 7])

# =========================
# PERCENT FUNCTION
# =========================
def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# HEADER
# =========================
left, middle, right = st.columns([2, 3, 1])

with left:
    st.markdown("""
    <h2 style="color:white;margin:0;">
        TQ & RFI Dashboard
    </h2>
    """, unsafe_allow_html=True)

with middle:
    st.markdown("""
    <p style="color:#9fb3c8;margin:10px 0 0 0;">
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
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">
Project Overview Analytics
</h3>
<p style="color:#9fb3c8;margin:5px 0 0 0;">
Not Responded within 7 days – TQ & RFI Ageing Overview
</p>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI BOXES (SMALL EXECUTIVE CARDS)
# =========================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Not Responded", len(tq_over), f"{pct(tq_over)}%")

with k2:
    st.metric("RFI Not Responded", len(rfi_over), f"{pct(rfi_over)}%")

with k3:
    st.metric("Both (Derived)", min(len(tq_over), len(rfi_over)), "-")

with k4:
    st.metric("Total >7 Days", total_overdue)

# =========================
# MAIN COMPARISON VISUAL (PROFESSIONAL)
# =========================

st.markdown("### TQ vs RFI Ageing Overview")

fig = go.Figure()

fig.add_trace(go.Bar(
    name="TQ Not Responded",
    x=["TQ"],
    y=[len(tq_over)],
    text=[f"{len(tq_over)} ({pct(tq_over)}%)"],
    textposition="auto",
    marker_color="#2F80ED"
))

fig.add_trace(go.Bar(
    name="RFI Not Responded",
    x=["RFI"],
    y=[len(rfi_over)],
    text=[f"{len(rfi_over)} ({pct(rfi_over)}%)"],
    textposition="auto",
    marker_color="#EB5757"
))

fig.update_layout(
    barmode="group",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    height=400,
    legend=dict(font=dict(color="white"))
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FINAL SUMMARY PANEL (SMALL BOX STYLE)
# =========================

st.markdown("### Summary Snapshot")

c1, c2, c3 = st.columns(3)

with c1:
    st.info(f"""
    **TQ Not Responded**  
    {len(tq_over)} items  
    {pct(tq_over)}%
    """)

with c2:
    st.info(f"""
    **RFI Not Responded**  
    {len(rfi_over)} items  
    {pct(rfi_over)}%
    """)

with c3:
    st.warning(f"""
    **Total Outstanding >7 Days**  
    {total_overdue} items  
    100%
    """)