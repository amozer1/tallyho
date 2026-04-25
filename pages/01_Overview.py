import streamlit as st
from datetime import datetime

st.markdown("---")

# =========================
# HEADER ROW (CLEAN EXECUTIVE STYLE)
# =========================
left, middle, right = st.columns([4, 2, 1.2])

with left:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        height:100%;
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
        height:100%;
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
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        text-align:center;
        height:100%;
    ">
        <div style="color:#00bfff;font-size:13px;font-weight:700;">
            Download
        </div>
        <div style="color:#9fb3c8;font-size:11px;margin-top:4px;">
            Report Export
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# KPI CALCULATIONS
# =========================
df["Status"] = df["Status"].astype(str).str.lower()

total_tq = len(df[df["Doc Type"] == "TQ"])
total_rfi = len(df[df["Doc Type"] == "RFI"])

open_items = len(df[df["Status"] == "open"])
closed_items = len(df[df["Status"] == "closed"])
outstanding_items = len(df[df["AgeDays"] > 7])

total_items = len(df)

sla_met = len(df[(df["AgeDays"] <= 7) & (df["Status"] == "closed")])
sla_pct = round((sla_met / total_items) * 100, 1) if total_items else 0

# =========================
# KPI CARDS ROW
# =========================
k1, k2, k3, k4, k5, k6 = st.columns(6)

card_style = """
    <div style="
        background:#0b1a2f;
        padding:14px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        text-align:center;
    ">
"""

with k1:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">Total TQs</div>
        <div style="color:white;font-size:22px;font-weight:800;">{total_tq}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">Total RFIs</div>
        <div style="color:white;font-size:22px;font-weight:800;">{total_rfi}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">Open Items</div>
        <div style="color:#FFA500;font-size:22px;font-weight:800;">{open_items}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">Closed Items</div>
        <div style="color:#00FFD5;font-size:22px;font-weight:800;">{closed_items}</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">Outstanding (>7 days)</div>
        <div style="color:#FF4B4B;font-size:22px;font-weight:800;">{outstanding_items}</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown(card_style + f"""
        <div style="color:#9fb3c8;font-size:12px;">SLA Performance</div>
        <div style="color:#00bfff;font-size:22px;font-weight:800;">{sla_pct}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")