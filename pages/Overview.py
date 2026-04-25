import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
from utils.data_loader import load_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="TQ & RFI Dashboard", layout="wide")

st.markdown("---")

# =========================
# LOAD DATA (MUST BE FIRST)
# =========================
df = load_data()
df.columns = df.columns.str.strip()

df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
today = pd.Timestamp.today().normalize()
df["AgeDays"] = (today - df["Date Sent"]).dt.days
df["Status"] = df["Status"].astype(str).str.lower()

# =========================
# SPLIT DATA
# =========================
tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

# =========================
# CLASSIFICATION FUNCTION
# =========================
def classify(data):
    open_items = data[(data["Status"] == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"] == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]
    return len(open_items), len(closed_items), len(outstanding_items)

tq_open, tq_closed, tq_outstanding = classify(tq)
rfi_open, rfi_closed, rfi_outstanding = classify(rfi)

# =========================
# TOTALS
# =========================
tq_total = len(tq)
rfi_total = len(rfi)
total_items = len(df)

def pct(x, total):
    return round((x / total) * 100, 1) if total else 0

# =========================
# HEADER (FIXED)
# =========================
left, middle, right = st.columns([4, 2, 1.5])

with left:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
    ">
        <div style="color:white;font-size:22px;font-weight:800;">
            TQ and RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;margin-top:4px;">
            Project Overview and Service Level Agreement Performance
        </div>
    </div>
    """, unsafe_allow_html=True)

with middle:
    st.markdown(f"""
    <div style="
        background:#0b1a2f;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        text-align:center;
    ">
        <div style="color:white;font-size:15px;font-weight:700;">
            {datetime.today().strftime('%d %b %Y')}
        </div>
        <div style="color:#9fb3c8;font-size:11px;margin-top:4px;">
            Last Updated
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.download_button(
        label="⬇ Download Report",
        data=df.to_excel(index=False, engine="openpyxl"),
        file_name=f"TQ_RFI_Report_{datetime.today().strftime('%d_%b_%Y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")

# =========================
# KPI SECTION
# =========================
open_items = len(df[df["Status"] == "open"])
closed_items = len(df[df["Status"] == "closed"])
outstanding_items = len(df[df["AgeDays"] > 7])

sla_met = len(df[(df["AgeDays"] <= 7) & (df["Status"] == "closed")])
sla_pct = round((sla_met / total_items) * 100, 1) if total_items else 0

k1, k2, k3, k4, k5 = st.columns(5)

card = """
<div style="
    background:#0b1a2f;
    padding:14px;
    border-radius:12px;
    border:1px solid rgba(0,191,255,0.2);
    text-align:center;
">
"""

with k1:
    st.markdown(card + f"<div style='color:white;font-size:20px'>{tq_total}</div><div style='color:#9fb3c8'>Total TQs</div></div>", unsafe_allow_html=True)

with k2:
    st.markdown(card + f"<div style='color:white;font-size:20px'>{rfi_total}</div><div style='color:#9fb3c8'>Total RFIs</div></div>", unsafe_allow_html=True)

with k3:
    st.markdown(card + f"<div style='color:#FFA500;font-size:20px'>{open_items}</div><div style='color:#9fb3c8'>Open Items</div></div>", unsafe_allow_html=True)

with k4:
    st.markdown(card + f"<div style='color:#00FFD5;font-size:20px'>{closed_items}</div><div style='color:#9fb3c8'>Closed Items</div></div>", unsafe_allow_html=True)

with k5:
    st.markdown(card + f"<div style='color:#FF4B4B;font-size:20px'>{outstanding_items}</div><div style='color:#9fb3c8'>Outstanding > 7 Days</div></div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# PLACEHOLDER FOR NEXT VISUAL LAYER
# =========================
st.markdown("""
### 📊 Next Section: SLA Visual Analytics (Circles / Trends / AI Insights)
""")