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
# FILTERS (>7 DAYS)
# =========================
tq_over = df[(df["Doc Type"] == "TQ") & (df["AgeDays"] > 7)]
rfi_over = df[(df["Doc Type"] == "RFI") & (df["AgeDays"] > 7)]

tq_count = len(tq_over)
rfi_count = len(rfi_over)

tq_set = set(tq_over["Recipient"])
rfi_set = set(rfi_over["Recipient"])

both_count = len(tq_set.intersection(rfi_set))

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
# KPI ROW (CLEAN BLOCKS)
# =========================
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:20px;border-radius:12px;">
        <h4 style="color:#2F80ED;margin:0;">TQ Not Responded</h4>
        <h2 style="color:white;margin:5px 0;">{tq_count}</h2>
        <p style="color:#9fb3c8;">{pct(tq_count)}% of overdue</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:20px;border-radius:12px;">
        <h4 style="color:#EB5757;margin:0;">RFI Not Responded</h4>
        <h2 style="color:white;margin:5px 0;">{rfi_count}</h2>
        <p style="color:#9fb3c8;">{pct(rfi_count)}% of overdue</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div style="background:#1b2b3a;padding:20px;border-radius:12px;">
        <h4 style="color:#00FFD5;margin:0;">Both (Overlap)</h4>
        <h2 style="color:white;margin:5px 0;">{both_count}</h2>
        <p style="color:#9fb3c8;">Shared recipients</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# SECOND ROW (INSIGHT + TOTAL)
# =========================
left, right = st.columns([2, 1])

with left:
    st.markdown(f"""
    <div style="background:#0b1a2f;padding:20px;border-radius:12px;">
        <h4 style="color:white;">Summary Insight</h4>
        <ul style="color:#9fb3c8;line-height:2;">
            <li>TQ Not Responded: {tq_count} ({pct(tq_count)}%)</li>
            <li>RFI Not Responded: {rfi_count} ({pct(rfi_count)}%)</li>
            <li>Both Overdue Recipients: {both_count}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="
        background:#1b2b3a;
        padding:25px;
        border-radius:12px;
        border-left:5px solid #2F80ED;
        text-align:center;
    ">
        <h4 style="color:white;">Total Outstanding</h4>
        <h1 style="color:white;margin:10px 0;">{total_overdue}</h1>
        <p style="color:#9fb3c8;">{pct(total_overdue)}% of dataset</p>
    </div>
    """, unsafe_allow_html=True)