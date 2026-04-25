import streamlit as st
import pandas as pd
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
# OVERDUE FILTER
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

# =========================
# BOTH RISK LOGIC
# =========================
tq_recipients = set(tq_over["Recipient"])
rfi_recipients = set(rfi_over["Recipient"])

both_recipients = tq_recipients.intersection(rfi_recipients)

both_risk = df[
    (df["Recipient"].isin(both_recipients)) &
    (df["AgeDays"] > 7)
]

# =========================
# TOTAL OVERDUE
# =========================
total_overdue = len(df[df["AgeDays"] > 7])

def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue else 0

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
# VENN STYLE CIRCLES (IMPROVED)
# =========================
st.markdown("""
<div style="
    position:relative;
    width:100%;
    height:260px;
    margin-top:20px;
    border:1px solid rgba(0,191,255,0.15);
    border-radius:18px;
    background:rgba(11,26,47,0.4);
">
""", unsafe_allow_html=True)

# LEFT CIRCLE (TQ)
st.markdown(f"""
<div style="
    position:absolute;
    left:18%;
    top:50px;
    width:140px;
    height:140px;
    border-radius:50%;
    background:rgba(0,150,255,0.18);
    border:2px solid #00bfff;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
">
    <div style="color:#00bfff;font-size:13px;font-weight:600;">TQ Overdue</div>
    <div style="color:white;font-size:22px;font-weight:bold;">{len(tq_over)}</div>
    <div style="color:#9fb3c8;font-size:12px;">{pct(tq_over)}%</div>
</div>
""", unsafe_allow_html=True)

# CENTER CIRCLE (BOTH RISK)
st.markdown(f"""
<div style="
    position:absolute;
    left:42%;
    top:30px;
    width:150px;
    height:150px;
    border-radius:50%;
    background:rgba(0,255,200,0.12);
    border:2px solid #00ffd5;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    z-index:2;
">
    <div style="color:#00ffd5;font-size:12px;font-weight:600;">
        Both Risk
    </div>
    <div style="color:white;font-size:22px;font-weight:bold;">
        {len(both_risk)}
    </div>
    <div style="color:#9fb3c8;font-size:12px;">
        {pct(both_risk)}%
    </div>
</div>
""", unsafe_allow_html=True)

# RIGHT CIRCLE (RFI)
st.markdown(f"""
<div style="
    position:absolute;
    right:18%;
    top:50px;
    width:140px;
    height:140px;
    border-radius:50%;
    background:rgba(255,100,255,0.12);
    border:2px solid #ff6bd6;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
">
    <div style="color:#ff6bd6;font-size:13px;font-weight:600;">RFI Overdue</div>
    <div style="color:white;font-size:22px;font-weight:bold;">{len(rfi_over)}</div>
    <div style="color:#9fb3c8;font-size:12px;">{pct(rfi_over)}%</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

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