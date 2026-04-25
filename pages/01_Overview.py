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

tq_set = set(tq_over.index)
rfi_set = set(rfi_over.index)

both_set = tq_set.intersection(rfi_set)

tq_only = len(tq_set - both_set)
rfi_only = len(rfi_set - both_set)
both = len(both_set)

total_overdue = len(df[df["AgeDays"] > 7])

def pct(x):
    return round((x / total_overdue) * 100, 1) if total_overdue else 0

# =========================
# HEADER
# =========================
left, middle, right = st.columns([2, 3, 1])

with left:
    st.markdown("<h2 style='color:white'>TQ & RFI Dashboard</h2>", unsafe_allow_html=True)

with middle:
    st.markdown("<p style='color:#9fb3c8'>Project Overview and Response Analytics</p>", unsafe_allow_html=True)

with right:
    st.markdown(f"<h4 style='color:white;text-align:right'>{datetime.today().strftime('%d %b %Y')}</h4>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECTION TITLE
# =========================
st.markdown("""
<h3 style="color:white;">Project Overview Analytics</h3>
<p style="color:#9fb3c8;">Not responded within 7 days – TQ & RFI ageing overview</p>
""", unsafe_allow_html=True)

# =========================
# MAIN LAYOUT (2 COLUMNS)
# =========================
left_col, right_col = st.columns([2, 1])

# =========================
# VENN STYLE (SIMULATED WITH PLOTLY)
# =========================
with left_col:

    fig = go.Figure()

    fig.add_shape(type="circle",
        x0=0, y0=0, x1=2, y1=2,
        line=dict(color="#2F80ED"),
    )

    fig.add_shape(type="circle",
        x0=1, y0=0, x1=3, y1=2,
        line=dict(color="#EB5757"),
    )

    fig.add_annotation(x=0.8, y=1.2,
        text=f"TQ Only<br>{tq_only} ({pct(tq_only)}%)",
        showarrow=False,
        font=dict(color="#2F80ED")
    )

    fig.add_annotation(x=2.2, y=1.2,
        text=f"RFI Only<br>{rfi_only} ({pct(rfi_only)}%)",
        showarrow=False,
        font=dict(color="#EB5757")
    )

    fig.add_annotation(x=1.5, y=0.8,
        text=f"Both<br>{both} ({pct(both)}%)",
        showarrow=False,
        font=dict(color="#00FFD5")
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
# RIGHT PANEL (KPI BULLETS)
# =========================
with right_col:

    st.markdown("### Breakdown")

    st.markdown(f"""
    <div style="color:white;line-height:2;">
        🔵 TQ Not Responded: <b>{tq_only}</b> ({pct(tq_only)}%)<br>
        🔴 RFI Not Responded: <b>{rfi_only}</b> ({pct(rfi_only)}%)<br>
        🟢 Both Overdue: <b>{both}</b> ({pct(both)}%)<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
    <div style="
        background:#1b2b3a;
        padding:15px;
        border-radius:12px;
        border:1px solid #2F80ED;
        color:white;
    ">
        <b>Total Outstanding > 7 Days</b><br><br>
        {total_overdue} items<br>
        {pct(total_overdue)}%
    </div>
    """, unsafe_allow_html=True)