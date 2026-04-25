import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.data_loader import load_data
from utils.metrics import get_metrics

# =========================
# LOAD DATA (YOUR EXCEL ONLY)
# =========================
df = load_data()
m = get_metrics(df)

st.set_page_config(layout="wide")

# =========================
# HEADER ROW
# =========================
left, right = st.columns([3, 1])

with left:
    st.markdown("""
    <div style="background:#0b1a2f;padding:15px;border-radius:12px;">
        <h2 style="color:white;">📊 TQ & RFI ML Dashboard</h2>
        <p style="color:#9fb3c8;">Project Overview and Response Analytics</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:15px;border-radius:12px;text-align:center;">
        <h4 style="color:white;">📅 {datetime.today().strftime("%d %b %Y")}</h4>
        <p style="color:#9fb3c8;">Download Report ⬇</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECTION A TITLE
# =========================
st.markdown("## A - Project Overview Analytics")

# =========================
# DERIVED METRICS (FROM YOUR DATA)
# =========================
today = pd.Timestamp.today().normalize()

df["AgeDays"] = (today - df["Date Sent"]).dt.days
df["IsClosed"] = df["Reply Date"].notna()

# Overdue > 7 days
overdue = df[df["AgeDays"] > 7]

tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

tq_over = len(tq[tq["AgeDays"] > 7])
rfi_over = len(rfi[rfi["AgeDays"] > 7])
both_over = min(tq_over, rfi_over)

total_overdue = len(overdue)

# =========================
# VENN-STYLE VISUAL (SIMPLIFIED BUT PROFESSIONAL)
# =========================
fig = go.Figure()

fig.add_shape(type="circle",
              x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0, 150, 255, 0.25)",
              line_color="blue")

fig.add_shape(type="circle",
              x0=1.2, y0=0, x1=3.2, y1=2,
              fillcolor="rgba(0, 255, 200, 0.25)",
              line_color="cyan")

fig.add_shape(type="circle",
              x0=0.6, y0=1, x1=2.6, y1=3,
              fillcolor="rgba(255, 100, 255, 0.25)",
              line_color="purple")

# Labels (YOUR REAL DATA ONLY)
fig.add_annotation(x=0.8, y=1.2, text=f"TQ Only<br>{tq_over}")
fig.add_annotation(x=2.2, y=1.2, text=f"RFI Only<br>{rfi_over}")
fig.add_annotation(x=1.7, y=2.2, text=f"Both<br>{both_over}")

fig.update_layout(
    height=350,
    template="plotly_dark",
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# KPI SUMMARY BOX (SMALL SQUARE PANEL)
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("TQ Overdue", tq_over)

with col2:
    st.metric("RFI Overdue", rfi_over)

with col3:
    st.metric("Both Overdue", both_over)

with col4:
    st.metric("Total > 7 Days", total_overdue)