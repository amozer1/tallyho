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
# FILTERS (>7 DAYS)
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

tq_count = len(tq_over)
rfi_count = len(rfi_over)

total_overdue = len(df[df["AgeDays"] > 7])

# BOTH (REAL OVERLAP)
both_count = len(
    set(tq_over["Recipient"]).intersection(set(rfi_over["Recipient"]))
)

def pct(x):
    return round((x / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# HEADER
# =========================
l, m, r = st.columns([2, 3, 1])

with l:
    st.markdown("<h2 style='color:white;'>TQ & RFI Dashboard</h2>", unsafe_allow_html=True)

with m:
    st.markdown("<p style='color:#9fb3c8;'>Project Overview and Response Analytics</p>", unsafe_allow_html=True)

with r:
    st.markdown(f"<h4 style='text-align:right;color:white;'>{datetime.today().strftime('%d %b %Y')}</h4>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECTION TITLE
# =========================
st.markdown("""
<h3 style="color:white;">Project Overview Analytics</h3>
<p style="color:#9fb3c8;">Not responded within 7 days – workload composition & ageing overview</p>
""", unsafe_allow_html=True)

# =========================
# KPI STRIP (STATUS ONLY)
# =========================
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:18px;border-radius:10px;">
        <h4 style="color:#2F80ED;margin:0;">TQ Overdue</h4>
        <h2 style="color:white;">{tq_count}</h2>
        <p style="color:#9fb3c8;">{pct(tq_count)}%</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:18px;border-radius:10px;">
        <h4 style="color:#EB5757;margin:0;">RFI Overdue</h4>
        <h2 style="color:white;">{rfi_count}</h2>
        <p style="color:#9fb3c8;">{pct(rfi_count)}%</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:18px;border-radius:10px;">
        <h4 style="color:white;margin:0;">Total Overdue</h4>
        <h2 style="color:white;">{total_overdue}</h2>
        <p style="color:#9fb3c8;">100%</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# WORKLOAD COMPOSITION BAR (FIXED IDEA)
# =========================
st.markdown("### Workload Composition (>7 Days)")

fig = go.Figure()

fig.add_trace(go.Bar(
    name="TQ Only",
    x=["Workload"],
    y=[tq_count],
    marker_color="#2F80ED",
    text=f"{tq_count}",
    textposition="auto"
))

fig.add_trace(go.Bar(
    name="RFI Only",
    x=["Workload"],
    y=[rfi_count],
    marker_color="#EB5757",
    text=f"{rfi_count}",
    textposition="auto"
))

fig.add_trace(go.Bar(
    name="Both (Overlap)",
    x=["Workload"],
    y=[both_count],
    marker_color="#00FFD5",
    text=f"{both_count}",
    textposition="auto"
))

fig.update_layout(
    barmode="stack",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    height=400,
    legend=dict(font=dict(color="white"))
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHT PANEL (NO REPETITION)
# =========================
st.markdown("### Key Insight")

st.markdown(f"""
<div style="
    background:#0b1a2f;
    padding:18px;
    border-radius:10px;
    border-left:4px solid #2F80ED;
    color:#9fb3c8;
    line-height:2;
">
✔ TQ contributes <b style="color:white">{pct(tq_count)}%</b> of overdue workload<br>
✔ RFI contributes <b style="color:white">{pct(rfi_count)}%</b><br>
✔ Overlap (same recipients) = <b style="color:white">{both_count}</b> items<br>
✔ Total risk backlog = <b style="color:white">{total_overdue}</b>
</div>
""", unsafe_allow_html=True)