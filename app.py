import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]
    return df

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])
default_path = "data/TQ_TH.xlsx"

df = load_data(uploaded_file) if uploaded_file else load_data(default_path)

# =========================
# CLEAN
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())
df["AgeDays"] = (now - df["Date Sent"]).dt.days.fillna(0)

is_tq = df["Doc Type"].str.contains("TQ", na=False)
is_rfi = df["Doc Type"].str.contains("RFI", na=False)

over_7 = df[df["AgeDays"] > 7]

# =========================
# KPIs
# =========================
tq_total = int(is_tq.sum())
rfi_total = int(is_rfi.sum())
overdue_7 = len(over_7)
open_total = len(df[df["Status"].str.contains("Open", case=False, na=False)])

# =========================
# A4 CONTROL CENTRE UI (NO STREAMLIT LAYOUT SYSTEM)
# =========================
html = f"""
<style>

body {{
    margin: 0;
}}

.dashboard {{
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    grid-template-rows: 80px 140px 200px 200px;
    gap: 10px;
    height: 95vh;
    font-family: Arial;
}}

/* HEADER */
.header {{
    grid-column: 1 / 3;
    background: #111827;
    color: white;
    padding: 10px 20px;
    display:flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 10px;
}}

/* KPI STRIP */
.kpi {{
    grid-column: 1 / 3;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}}

.card {{
    background: #f4f6f8;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}}

.big {{
    font-size: 22px;
    font-weight: bold;
}}

.label {{
    font-size: 12px;
    color: #666;
}}

/* MAIN GRID */
.a {{
    background: #e8f0fe;
    border-radius: 12px;
    padding: 10px;
}}

.b {{
    background: #fff4e6;
    border-radius: 12px;
    padding: 10px;
}}

.c {{
    background: #e6fffa;
    border-radius: 12px;
    padding: 10px;
}}

.d {{
    background: #fef3f3;
    border-radius: 12px;
    padding: 10px;
}}

.e {{
    background: #f3f4f6;
    border-radius: 12px;
    padding: 10px;
}}

</style>

<div class="dashboard">

<!-- HEADER -->
<div class="header">
    <div><b>TQ & RFI EXECUTIVE CONTROL CENTRE</b></div>
    <div>{datetime.now().strftime("%d %b %Y")}</div>
</div>

<!-- KPI ROW -->
<div class="kpi">

    <div class="card">
        <div class="big">{overdue_7}</div>
        <div class="label">Overdue >7 Days</div>
    </div>

    <div class="card">
        <div class="big">{tq_total}</div>
        <div class="label">Total TQs</div>
    </div>

    <div class="card">
        <div class="big">{rfi_total}</div>
        <div class="label">Total RFIs</div>
    </div>

    <div class="card">
        <div class="big">{open_total}</div>
        <div class="label">Open Items</div>
    </div>

</div>

<!-- A -->
<div class="a">
    <b>A - Project Overview</b><br><br>
    • Overdue (>7 days): {overdue_7}<br>
    • System backlog active control view<br>
    • TQ vs RFI distribution active
</div>

<!-- B -->
<div class="b">
    <b>B - KPI Control</b><br><br>
    • Live open workload<br>
    • System pressure indicator<br>
    • Delivery status summary
</div>

<!-- C -->
<div class="c">
    <b>C - Trend Control</b><br><br>
    • TQ & RFI flow over time<br>
    • Delivery activity monitoring
</div>

<!-- D -->
<div class="d">
    <b>D - Ageing Heat Map</b><br><br>
    • 0-2 / 3-7 / 8-14 / 15-30 / 30+<br>
    • Backlog intensity view
</div>

<!-- E -->
<div class="e">
    <b>E - AI Risk Engine</b><br><br>
    • Risk: {round((overdue_7/len(df))*100,1) if len(df)>0 else 0}%<br>
    • Delay probability model<br>
    • Executive alert system
</div>

</div>
"""

st.components.v1.html(html, height=900, scrolling=False)