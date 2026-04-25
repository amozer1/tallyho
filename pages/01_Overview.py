import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_loader import load_data

# =========================
# LOAD DATA (YOUR FILE ONLY)
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

# =========================
# "BOTH RISK" LOGIC (REALISTIC)
# Same recipient has BOTH overdue TQ and RFI
# =========================
tq_recipients = set(tq_over["Recipient"])
rfi_recipients = set(rfi_over["Recipient"])

both_recipients = tq_recipients.intersection(rfi_recipients)
both_risk = df[
    (df["Recipient"].isin(both_recipients)) &
    (df["AgeDays"] > 7)
]

# =========================
# TOTAL OVERDUE BASELINE
# =========================
total_overdue = len(df[df["AgeDays"] > 7])

def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue > 0 else 0

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
# SECTION TITLE
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
">
<h3 style="color:white;margin:0;">A - Project Overview Analytics</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# 3 CLEAN INSIGHT CIRCLES
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div style="
        width:160px;height:160px;border-radius:50%;
        background:rgba(0,150,255,0.15);
        border:2px solid #00bfff;
        display:flex;flex-direction:column;
        align-items:center;justify-content:center;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#00bfff;font-size:13px;font-weight:600;">
            TQ Overdue
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {len(tq_over)}
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            {pct(tq_over)}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
        width:160px;height:160px;border-radius:50%;
        background:rgba(0,255,200,0.12);
        border:2px solid #00ffd5;
        display:flex;flex-direction:column;
        align-items:center;justify-content:center;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#00ffd5;font-size:13px;font-weight:600;">
            Both Risk (Same Recipient)
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {len(both_risk)}
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            {pct(both_risk)}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="
        width:160px;height:160px;border-radius:50%;
        background:rgba(255,100,255,0.12);
        border:2px solid #ff6bd6;
        display:flex;flex-direction:column;
        align-items:center;justify-content:center;
        margin:auto;
        text-align:center;
    ">
        <div style="color:#ff6bd6;font-size:13px;font-weight:600;">
            RFI Overdue
        </div>
        <div style="color:white;font-size:22px;font-weight:bold;">
            {len(rfi_over)}
        </div>
        <div style="color:#9fb3c8;font-size:12px;">
            {pct(rfi_over)}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KPI STRIP
# =========================
st.markdown("---")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Overdue", len(tq_over))

with k2:
    st.metric("RFI Overdue", len(rfi_over))

with k3:
    st.metric("High Risk Recipients", len(both_recipients))

with k4:
    st.metric("Total Overdue", total_overdue)