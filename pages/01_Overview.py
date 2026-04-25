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

# =========================
# SAFETY CLEANING (NO ERRORS)
# =========================
df.columns = df.columns.str.strip()

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

both_over = df[(df["AgeDays"] > 7)]

total_overdue = len(both_over)

# =========================
# HEADER (TOP ROW)
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
# SECTION A TITLE BOX
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
# CALCULATIONS (SAFE)
# =========================
def pct(part, total):
    return round((len(part) / total) * 100, 1) if total > 0 else 0

overdue_total = df[df["AgeDays"] > 7]

tq_pct = pct(tq_over, len(overdue_total))
rfi_pct = pct(rfi_over, len(overdue_total))
both_pct = pct(both_over, len(overdue_total))

# =========================
# CLEAN ANALYTICS PANEL
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div style="
        background:#08172a;
        padding:22px;
        border-radius:12px;
        border:1px solid rgba(0,150,255,0.4);
        text-align:center;
    ">
        <h4 style="color:#00bfff;">TQ Only</h4>
        <h1 style="color:white;margin:0;">{tq_pct}%</h1>
        <p style="color:#9fb3c8;">({len(tq_over)} items)</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
        background:#08172a;
        padding:22px;
        border-radius:12px;
        border:1px solid rgba(0,255,200,0.4);
        text-align:center;
    ">
        <h4 style="color:#00ffd5;">Both TQ & RFI</h4>
        <h1 style="color:white;margin:0;">{both_pct}%</h1>
        <p style="color:#9fb3c8;">({len(both_over)} items)</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="
        background:#08172a;
        padding:22px;
        border-radius:12px;
        border:1px solid rgba(255,100,255,0.4);
        text-align:center;
    ">
        <h4 style="color:#ff6bd6;">RFI Only</h4>
        <h1 style="color:white;margin:0;">{rfi_pct}%</h1>
        <p style="color:#9fb3c8;">({len(rfi_over)} items)</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SMALL SUMMARY STRIP (BOTTOM OF SECTION A)
# =========================
st.markdown("---")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("TQ Overdue", len(tq_over))

with s2:
    st.metric("RFI Overdue", len(rfi_over))

with s3:
    st.metric("Both Overdue", len(both_over))

with s4:
    st.metric("Total > 7 Days", len(overdue_total))