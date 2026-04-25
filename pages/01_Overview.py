import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(page_title="Overview", layout="wide")

# =========================
# LOAD REAL DATA ONLY
# =========================
df = load_data()
m = get_metrics(df)

# Safety check (REAL DATA ONLY)
if df.empty:
    st.warning("No data loaded from Excel file.")
    st.stop()

# =========================
# HEADER (NO PLACEHOLDERS)
# =========================
st.title("📊 TQ & RFI Overview Dashboard")
st.caption(f"Last Updated: {datetime.today().strftime('%d %b %Y %H:%M')}")

# =========================
# KPI ROW (FROM YOUR DATA ONLY)
# =========================
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total TQs", m["total_tq"])
c2.metric("Total RFIs", m["total_rfi"])
c3.metric("Closed Items", m["closed"])
c4.metric("Open Items", m["open"])
c5.metric("Overdue (>7 days)", m["overdue7"])

st.markdown("---")

# =========================
# REAL INSIGHT LOGIC (NO FAKE MODEL)
# =========================

# True overdue calculation from YOUR columns
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
df["Required Date"] = pd.to_datetime(df["Required Date"], errors="coerce", dayfirst=True)
df["Reply Date"] = pd.to_datetime(df["Reply Date"], errors="coerce", dayfirst=True)

today = pd.Timestamp.today().normalize()

df["IsOverdue"] = df["Reply Date"].isna() & (df["Required Date"] < today)

overdue_by_recipient = df[df["IsOverdue"]]["Recipient"].value_counts().head(5)

# =========================
# REAL INSIGHT DISPLAY
# =========================
st.subheader("📌 Key Insights (From Your Data)")

if m["overdue7"] > 0:
    st.error(f"{m['overdue7']} items are overdue based on Required Date logic.")
else:
    st.success("No overdue items detected based on current dataset.")

st.markdown("### Top Recipients with Overdue Items")

st.dataframe(overdue_by_recipient)

# =========================
# REAL WORKLOAD VIEW
# =========================
st.markdown("### Workload Distribution (Real Data)")

workload = df["Recipient"].value_counts().reset_index()
workload.columns = ["Recipient", "Count"]

st.bar_chart(workload.set_index("Recipient"))