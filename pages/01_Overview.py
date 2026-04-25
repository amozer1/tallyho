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
# SPLIT
# =========================
tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

def classify(data):
    open_items = data[(data["Status"].str.lower() == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"].str.lower() == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]
    return len(open_items), len(closed_items), len(outstanding_items)

tq_open, tq_closed, tq_out = classify(tq)
rfi_open, rfi_closed, rfi_out = classify(rfi)

def pct(x, total):
    return round((x / total) * 100, 1) if total else 0

tq_total = len(tq)
rfi_total = len(rfi)

# =========================
# HEADER
# =========================
st.markdown(f"""
<h2 style="color:white;">TQ & RFI Dashboard</h2>
<p style="color:#9fb3c8;">Project Overview & SLA Performance</p>
<h4 style="color:white;text-align:right;">{datetime.today().strftime('%d %b %Y')}</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# FUNCTION: TRUE SEGMENTED RING
# =========================
def ring(title, open_v, closed_v, out_v, total, color):
    return f"""
    <div style="display:flex;justify-content:center;margin:20px;">
    <svg width="320" height="320" viewBox="0 0 36 36">

        <!-- BACKGROUND RING -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#1b2b3a" stroke-width="3.8" />

        <!-- OPEN -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#FFA500" stroke-width="3.8"
            stroke-dasharray="{pct(open_v,total)} {100-pct(open_v,total)}"
            transform="rotate(-90 18 18)" />

        <!-- CLOSED -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#00FFD5" stroke-width="3.8"
            stroke-dasharray="{pct(closed_v,total)} {100-pct(closed_v,total)}"
            stroke-dashoffset="-{pct(open_v,total)}"
            transform="rotate(-90 18 18)" />

        <!-- OUTSTANDING -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#FF4B4B" stroke-width="3.8"
            stroke-dasharray="{pct(out_v,total)} {100-pct(out_v,total)}"
            stroke-dashoffset="-{pct(open_v,total)+pct(closed_v,total)}"
            transform="rotate(-90 18 18)" />

        <!-- TEXT INSIDE CENTER -->
        <text x="18" y="16" text-anchor="middle" fill="white" font-size="2.5">
            {title}
        </text>

        <text x="18" y="19" text-anchor="middle" fill="white" font-size="1.8">
            Total: {total}
        </text>

        <text x="18" y="22" text-anchor="middle" fill="#FFA500" font-size="1.4">
            Open {open_v} ({pct(open_v,total)}%)
        </text>

        <text x="18" y="24" text-anchor="middle" fill="#00FFD5" font-size="1.4">
            Closed {closed_v} ({pct(closed_v,total)}%)
        </text>

        <text x="18" y="26" text-anchor="middle" fill="#FF4B4B" font-size="1.4">
            Out {out_v} ({pct(out_v,total)}%)
        </text>

    </svg>
    </div>
    """

# =========================
# DISPLAY TWO RINGS
# =========================
c1, c2 = st.columns(2)

with c1:
    st.markdown("### TQ Lifecycle", unsafe_allow_html=True)
    st.markdown(ring("TQ", tq_open, tq_closed, tq_out, tq_total, "#FFA500"), unsafe_allow_html=True)

with c2:
    st.markdown("### RFI Lifecycle", unsafe_allow_html=True)
    st.markdown(ring("RFI", rfi_open, rfi_closed, rfi_out, rfi_total, "#2F80ED"), unsafe_allow_html=True)