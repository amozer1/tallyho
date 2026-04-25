import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
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

tq_count = len(tq_over)
rfi_count = len(rfi_over)

# overlap logic (based on Recipient)
tq_set = set(tq_over["Recipient"])
rfi_set = set(rfi_over["Recipient"])

both_set = tq_set.intersection(rfi_set)

both_count = len(both_set)

total_overdue = len(df[df["AgeDays"] > 7])

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
<p style="color:#9fb3c8;">Not responded within 7 days – TQ & RFI ageing overview</p>
""", unsafe_allow_html=True)

# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([2.2, 1])

# =========================
# VENN DIAGRAM (PROPER CLEAN VERSION)
# =========================
with left:

    fig = go.Figure()

    # Left circle (TQ)
    fig.add_shape(type="circle",
        x0=0.5, y0=0.5, x1=3, y1=3,
        line=dict(color="#2F80ED", width=3),
    )

    # Right circle (RFI)
    fig.add_shape(type="circle",
        x0=2, y0=0.5, x1=4.5, y1=3,
        line=dict(color="#EB5757", width=3),
    )

    # Labels
    fig.add_annotation(x=1.3, y=2,
        text=f"TQ<br>{tq_count} ({pct(tq_count)}%)",
        showarrow=False,
        font=dict(color="#2F80ED", size=14)
    )

    fig.add_annotation(x=3.2, y=2,
        text=f"RFI<br>{rfi_count} ({pct(rfi_count)}%)",
        showarrow=False,
        font=dict(color="#EB5757", size=14)
    )

    fig.add_annotation(x=2.4, y=1.5,
        text=f"Both<br>{both_count}",
        showarrow=False,
        font=dict(color="#00FFD5", size=13)
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="#0b1a2f",
        plot_bgcolor="#0b1a2f",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# RIGHT PANEL (CLEAN KPI LIST)
# =========================
with right:

    st.markdown("### Breakdown")

    st.markdown(f"""
    <div style="color:white;line-height:2;font-size:15px;">
        🔵 TQ Not Responded: <b>{tq_count}</b> ({pct(tq_count)}%)<br>
        🔴 RFI Not Responded: <b>{rfi_count}</b> ({pct(rfi_count)}%)<br>
        🟢 Both (Overlap): <b>{both_count}</b><br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
    <div style="
        background:#1b2b3a;
        padding:15px;
        border-radius:12px;
        border-left:4px solid #2F80ED;
        color:white;
    ">
        <b>Total Outstanding &gt; 7 Days</b><br><br>
        {total_overdue} items<br>
        {pct(total_overdue)}%
    </div>
    """, unsafe_allow_html=True)