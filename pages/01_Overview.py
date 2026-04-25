import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_loader import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()
df.columns = df.columns.str.strip()

df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
today = pd.Timestamp.today().normalize()
df["AgeDays"] = (today - df["Date Sent"]).dt.days

# =========================
# FILTERS (REAL DATA ONLY)
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

tq_recipients = set(tq_over["Recipient"])
rfi_recipients = set(rfi_over["Recipient"])

both_recipients = tq_recipients.intersection(rfi_recipients)

both_risk = df[
    (df["Recipient"].isin(both_recipients)) &
    (df["AgeDays"] > 7)
]

total_overdue = len(df[df["AgeDays"] > 7])

def pct(x):
    return round((len(x) / total_overdue) * 100, 1) if total_overdue > 0 else 0

# =========================
# TITLE CARD
# =========================
st.markdown("""
<div style="
    background:#0b1a2f;
    padding:10px 14px;
    border-radius:10px;
    border:1px solid rgba(0,191,255,0.2);
    margin-bottom:12px;
">
<h3 style="color:white;margin:0;">A - Project Overview Analytics</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# BOUNDED PANEL (IMPORTANT)
# =========================
st.markdown("""
<div style="
    background:#081521;
    border:1px solid rgba(0,191,255,0.25);
    border-radius:16px;
    padding:18px;
">
""", unsafe_allow_html=True)

# =========================
# SMALL CIRCLES ROW (CLOSER + SMALLER)
# =========================
c1, c2, c3 = st.columns([1, 1, 1], gap="small")

circle_style = """
    width:110px;
    height:110px;
    border-radius:50%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    margin:auto;
    text-align:center;
"""

with c1:
    st.markdown(f"""
    <div style="{circle_style} background:rgba(0,150,255,0.18); border:2px solid #00bfff;">
        <div style="color:#00bfff;font-size:11px;">TQ</div>
        <div style="color:white;font-size:18px;font-weight:bold;">{len(tq_over)}</div>
        <div style="color:#9fb3c8;font-size:10px;">{pct(tq_over)}%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="{circle_style} background:rgba(0,255,200,0.12); border:2px solid #00ffd5;">
        <div style="color:#00ffd5;font-size:11px;">Both Risk</div>
        <div style="color:white;font-size:18px;font-weight:bold;">{len(both_risk)}</div>
        <div style="color:#9fb3c8;font-size:10px;">{pct(both_risk)}%</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="{circle_style} background:rgba(255,100,255,0.12); border:2px solid #ff6bd6;">
        <div style="color:#ff6bd6;font-size:11px;">RFI</div>
        <div style="color:white;font-size:18px;font-weight:bold;">{len(rfi_over)}</div>
        <div style="color:#9fb3c8;font-size:10px;">{pct(rfi_over)}%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOTTOM SUMMARY STRIP
# =========================
st.markdown("<br>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("TQ Overdue", len(tq_over))

with k2:
    st.metric("RFI Overdue", len(rfi_over))

with k3:
    st.metric("High Risk Recipients", len(both_recipients))

with k4:
    st.metric("Total Overdue", total_overdue)

# =========================
# CLOSE PANEL
# =========================
st.markdown("</div>", unsafe_allow_html=True)