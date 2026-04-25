import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_loader import load_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide", page_title="TQ & RFI Dashboard")

# =========================
# LOAD DATA (YOUR EXCEL ONLY)
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
# FILTERS
# =========================
tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

tq_over = tq[tq["AgeDays"] > 7]
rfi_over = rfi[rfi["AgeDays"] > 7]

both_over = df[df["AgeDays"] > 7]

# total overdue baseline
total_overdue = len(both_over)

def pct(value):
    return round((len(value) / total_overdue) * 100, 1) if total_overdue > 0 else 0

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
# SECTION A TITLE
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:12px;
    border-radius:10px;
    border:1px solid rgba(0,191,255,0.2);
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">
A - Project Overview Analytics
</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# CIRCULAR KPI CHIPS
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div style="
        width:150px;
        height:150px;
        border-radius:50%;
        background:rgba(0,150,255,0.15);
        border:2px solid #00bfff;
        display:flex;
        align-items:center;
        justify-content:center;
        flex-direction:column;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#00bfff;font-size:14px;font-weight:600;">
            TQ Only
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {pct(tq_over)}%
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            ({len(tq_over)})
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
        width:150px;
        height:150px;
        border-radius:50%;
        background:rgba(0,255,200,0.12);
        border:2px solid #00ffd5;
        display:flex;
        align-items:center;
        justify-content:center;
        flex-direction:column;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#00ffd5;font-size:14px;font-weight:600;">
            Both
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {pct(both_over)}%
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            ({len(both_over)})
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="
        width:150px;
        height:150px;
        border-radius:50%;
        background:rgba(255,100,255,0.12);
        border:2px solid #ff6bd6;
        display:flex;
        align-items:center;
        justify-content:center;
        flex-direction:column;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#ff6bd6;font-size:14px;font-weight:600;">
            RFI Only
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {pct(rfi_over)}%
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            ({len(rfi_over)})
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SMALL KPI STRIP (BOTTOM SUMMARY)
# =========================
st.markdown("---")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Overdue", len(tq_over))

with k2:
    st.metric("RFI Overdue", len(rfi_over))

with k3:
    st.metric("Total Overdue", len(both_over))

with k4:
    st.metric("Total Records", len(df))