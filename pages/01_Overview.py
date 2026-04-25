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
# BASIC METRICS (for later use)
# =========================
tq_df = df[df["Doc Type"] == "TQ"]
rfi_df = df[df["Doc Type"] == "RFI"]

total_tq = len(tq_df)
total_rfi = len(rfi_df)
total_open = len(df[df["Status"].str.lower() == "open"])
total_closed = len(df[df["Status"].str.lower() == "closed"])
total_outstanding = len(df[df["AgeDays"] > 7])

# =========================
# HEADER (EXECUTIVE STYLE)
# =========================
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #0b1a2f, #0f2747);
    padding: 18px 22px;
    border-radius: 16px;
    border: 1px solid rgba(0,191,255,0.25);
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    display: flex;
    justify-content: space-between;
    align-items: center;
">

    <!-- LEFT -->
    <div>
        <div style="
            color: white;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 0.5px;
        ">
            📊 TQ & RFI Dashboard
        </div>
        <div style="
            color: #9fb3c8;
            font-size: 13px;
            margin-top: 4px;
        ">
            Project Overview & SLA Performance Analytics
        </div>
    </div>

    <!-- RIGHT -->
    <div style="text-align:right;">
        <div style="
            color: white;
            font-size: 14px;
            font-weight: 600;
        ">
            📅 {date}
        </div>
        <div style="
            color: #9fb3c8;
            font-size: 12px;
            margin-top: 4px;
        ">
            Live Project Intelligence
        </div>
    </div>

</div>
""".format(date=datetime.today().strftime('%d %b %Y')), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI STRIP (UNDER HEADER)
# =========================
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:12px;border-radius:12px;
    border:1px solid rgba(0,191,255,0.15);text-align:center;">
        <div style="color:#9fb3c8;font-size:12px;">Total TQs</div>
        <div style="color:white;font-size:20px;font-weight:700;">{total_tq}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:12px;border-radius:12px;
    border:1px solid rgba(0,191,255,0.15);text-align:center;">
        <div style="color:#9fb3c8;font-size:12px;">Total RFIs</div>
        <div style="color:white;font-size:20px;font-weight:700;">{total_rfi}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:12px;border-radius:12px;
    border:1px solid rgba(255,165,0,0.2);text-align:center;">
        <div style="color:#9fb3c8;font-size:12px;">Open Items</div>
        <div style="color:#FFA500;font-size:20px;font-weight:700;">{total_open}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:12px;border-radius:12px;
    border:1px solid rgba(255,75,75,0.2);text-align:center;">
        <div style="color:#9fb3c8;font-size:12px;">Outstanding >7d</div>
        <div style="color:#FF4B4B;font-size:20px;font-weight:700;">{total_outstanding}</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:12px;border-radius:12px;
    border:1px solid rgba(0,255,213,0.2);text-align:center;">
        <div style="color:#9fb3c8;font-size:12px;">Closed</div>
        <div style="color:#00FFD5;font-size:20px;font-weight:700;">{total_closed}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)