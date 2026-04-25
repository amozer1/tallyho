import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
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
# SPLIT DATA
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
# HEADER (IMPROVED + PROFESSIONAL)
# =========================
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #0b1a2f, #0f2747);
    padding: 18px 22px;
    border-radius: 14px;
    border: 1px solid rgba(0,191,255,0.35);
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
">

    <div style="display:flex;justify-content:space-between;align-items:center;">

        <!-- LEFT -->
        <div>
            <div style="color:white;font-size:22px;font-weight:800;">
                TQ and RFI Dashboard
            </div>
            <div style="color:#9fb3c8;font-size:13px;margin-top:4px;">
                Project Overview and Service Level Agreement Performance
            </div>
        </div>

        <!-- RIGHT -->
        <div style="text-align:right;">
            <div style="color:white;font-size:15px;font-weight:600;">
                {datetime.today().strftime('%d %b %Y')}
            </div>
            <div style="color:#9fb3c8;font-size:12px;margin-top:4px;">
                Last Updated
            </div>
        </div>

    </div>

</div>

<hr style="
    margin-top:14px;
    margin-bottom:20px;
    border:none;
    height:1px;
    background:linear-gradient(to right, transparent, #00bfff55, transparent);
">
""", unsafe_allow_html=True)

# =========================
# SAFE SVG RING FUNCTION (UNCHANGED)
# =========================
def render_ring(title, open_v, closed_v, out_v, total, color):

    return f"""
    <div style="display:flex;justify-content:center;">
    <svg width="320" height="320" viewBox="0 0 36 36">

        <!-- BACKGROUND -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#1b2b3a" stroke-width="3.8"/>

        <!-- OPEN -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#FFA500" stroke-width="3.8"
            stroke-dasharray="{pct(open_v,total)} 100"
            transform="rotate(-90 18 18)"/>

        <!-- CLOSED -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#00FFD5" stroke-width="3.8"
            stroke-dasharray="{pct(closed_v,total)} 100"
            stroke-dashoffset="-{pct(open_v,total)}"
            transform="rotate(-90 18 18)"/>

        <!-- OUTSTANDING -->
        <circle cx="18" cy="18" r="15.915" fill="none"
            stroke="#FF4B4B" stroke-width="3.8"
            stroke-dasharray="{pct(out_v,total)} 100"
            stroke-dashoffset="-{pct(open_v,total)+pct(closed_v,total)}"
            transform="rotate(-90 18 18)"/>

        <!-- CENTER TEXT -->
        <text x="18" y="15" text-anchor="middle" fill="white" font-size="2.5">{title}</text>
        <text x="18" y="18" text-anchor="middle" fill="white" font-size="1.8">Total: {total}</text>

        <text x="18" y="21" text-anchor="middle" fill="#FFA500" font-size="1.3">
            Open {open_v} ({pct(open_v,total)}%)
        </text>

        <text x="18" y="23" text-anchor="middle" fill="#00FFD5" font-size="1.3">
            Closed {closed_v} ({pct(closed_v,total)}%)
        </text>

        <text x="18" y="25" text-anchor="middle" fill="#FF4B4B" font-size="1.3">
            Out {out_v} ({pct(out_v,total)}%)
        </text>

    </svg>
    </div>
    """

# =========================
# CIRCLES DISPLAY (UNCHANGED)
# =========================
c1, c2 = st.columns(2)

with c1:
    components.html(render_ring("TQ", tq_open, tq_closed, tq_out, tq_total, "#FFA500"), height=380)

with c2:
    components.html(render_ring("RFI", rfi_open, rfi_closed, rfi_out, rfi_total, "#2F80ED"), height=380)