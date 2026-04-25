import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
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
# SPLIT
# =========================
tq_df = df[df["Doc Type"] == "TQ"]
rfi_df = df[df["Doc Type"] == "RFI"]

# =========================
# CLASSIFICATION
# =========================
def classify(data):
    open_items = data[(data["Status"].str.lower() == "open") & (data["AgeDays"] <= 7)]
    closed_items = data[data["Status"].str.lower() == "closed"]
    outstanding_items = data[data["AgeDays"] > 7]
    return len(open_items), len(closed_items), len(outstanding_items)

tq_open, tq_closed, tq_outstanding = classify(tq_df)
rfi_open, rfi_closed, rfi_outstanding = classify(rfi_df)

# =========================
# TOTALS
# =========================
tq_total = tq_open + tq_closed + tq_outstanding
rfi_total = rfi_open + rfi_closed + rfi_outstanding

# =========================
# PERCENT FUNCTION
# =========================
def pct(val, total):
    return round((val / total) * 100, 1) if total else 0

# =========================
# HEADER
# =========================
l, m, r = st.columns([2, 3, 1])

with l:
    st.markdown("<h2 style='color:white;'>TQ & RFI Dashboard</h2>", unsafe_allow_html=True)

with m:
    st.markdown("<p style='color:#9fb3c8;'>Project Overview & SLA Performance</p>", unsafe_allow_html=True)

with r:
    st.markdown(f"<h4 style='text-align:right;color:white;'>{datetime.today().strftime('%d %b %Y')}</h4>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# CAKE DONUT FUNCTION
# =========================
def cake_donut(title, open_v, closed_v, outstanding_v, total):
    fig = go.Figure(data=[go.Pie(
        labels=["Open", "Closed", "Outstanding"],
        values=[open_v, closed_v, outstanding_v],
        hole=0.65,   # thick "cake"
        marker=dict(colors=["#FFA500", "#00FFD5", "#FF4B4B"]),
        textinfo="none"   # IMPORTANT: remove outer text
    )])

    # Central annotation (THIS is the key)
    fig.update_layout(
        title=title,
        paper_bgcolor="#0b1a2f",
        font=dict(color="white"),
        height=380,
        annotations=[
            dict(
                text=f"""
                <b>{title}</b><br>
                Total: {total}<br>
                Open: {open_v} ({pct(open_v, total)}%)<br>
                Closed: {closed_v} ({pct(closed_v, total)}%)<br>
                Overdue: {outstanding_v} ({pct(outstanding_v, total)}%)
                """,
                x=0.5,
                y=0.5,
                font=dict(size=14, color="white"),
                showarrow=False,
                align="center"
            )
        ],
        showlegend=True,
        legend=dict(font=dict(color="white"))
    )

    return fig

# =========================
# LAYOUT
# =========================
c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        cake_donut("TQ", tq_open, tq_closed, tq_outstanding, tq_total),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        cake_donut("RFI", rfi_open, rfi_closed, rfi_outstanding, rfi_total),
        use_container_width=True
    )