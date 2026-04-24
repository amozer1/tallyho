import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
default_path = "data/TQ_TH.xlsx"

df = load_data(uploaded_file) if uploaded_file else load_data(default_path)

# =========================
# CLEAN DATA
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
df["Reply Date"] = pd.to_datetime(df["Reply Date"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())
df["AgeDays"] = (now - df["Date Sent"]).dt.days.fillna(0)

df["Doc Type"] = df["Doc Type"].str.upper()

is_tq = df["Doc Type"].str.contains("TQ", na=False)
is_rfi = df["Doc Type"].str.contains("RFI", na=False)

overdue_7 = df[df["AgeDays"] > 7]
overdue_30 = df[df["AgeDays"] > 30]

risk = round((len(overdue_7) / len(df)) * 100, 1) if len(df) > 0 else 0

# =========================
# NAVIGATION
# =========================
page = st.sidebar.radio(
    "Navigation",
    ["🟦 Executive Control Centre", "🟩 Data Explorer"]
)

# ==========================================================
# 🟦 PAGE 1 - EXECUTIVE CONTROL CENTRE (A4 DASHBOARD)
# ==========================================================
if page == "🟦 Executive Control Centre":

    st.markdown("""
    <style>
    .header {
        background:#111827;
        color:white;
        padding:12px;
        border-radius:10px;
        display:flex;
        justify-content:space-between;
        font-family:Arial;
    }
    .kpi {
        background:#f3f4f6;
        padding:10px;
        border-radius:10px;
        text-align:center;
        font-weight:bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown(f"""
    <div class="header">
        <div><b>TQ & RFI EXECUTIVE CONTROL CENTRE</b></div>
        <div>{datetime.now().strftime("%d %b %Y")}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # KPI ROW
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='kpi'>Overdue >7<br>{len(overdue_7)}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'>TQ<br>{int(is_tq.sum())}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'>RFI<br>{int(is_rfi.sum())}</div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi'>Risk %<br>{risk}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # MAIN GRID
    a, b = st.columns([2, 1])

    # PIE (A)
    with a:
        st.subheader("A - TQ vs RFI Overview")

        pie_df = pd.DataFrame({
            "Type": ["TQ", "RFI"],
            "Count": [is_tq.sum(), is_rfi.sum()]
        })

        fig1 = px.pie(pie_df, names="Type", values="Count", hole=0.5)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("C - Trend Analysis")

        trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

        fig2 = go.Figure()

        if "TQ" in trend.columns:
            fig2.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))
        if "RFI" in trend.columns:
            fig2.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

        st.plotly_chart(fig2, use_container_width=True)

    # RIGHT PANEL (B + D + E)
    with b:
        st.subheader("B - KPI Intelligence")

        st.metric("Total Items", len(df))
        st.metric("Overdue >7", len(overdue_7))
        st.metric("Overdue >30", len(overdue_30))

        st.markdown("---")

        st.subheader("D - Ageing")

        bins = [0, 2, 7, 14, 30, 999]
        labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

        df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
        age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

        st.bar_chart(age)

        st.markdown("---")

        st.subheader("E - AI Risk")

        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            title={"text": "Delay Risk %"},
            gauge={"axis": {"range": [0, 100]}}
        ))

        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    st.subheader("🧠 Executive Insights")

    col1, col2 = st.columns(2)

    col1.warning(f"{len(overdue_7)} items overdue >7 days")
    col2.info(f"Highest sender workload: {df['Sender'].value_counts().idxmax()}")

# ==========================================================
# 🟩 PAGE 2 - DATA EXPLORER (FULL OPERATIONS LAYER)
# ==========================================================
elif page == "🟩 Data Explorer":

    st.title("📋 Data Explorer - TQ & RFI Operations")

    st.sidebar.header("Filters")

    doc_filter = st.sidebar.multiselect(
        "Doc Type",
        df["Doc Type"].unique(),
        df["Doc Type"].unique()
    )

    status_filter = st.sidebar.multiselect(
        "Status",
        df["Status"].unique(),
        df["Status"].unique()
    )

    sender_filter = st.sidebar.multiselect(
        "Sender",
        df["Sender"].unique(),
        df["Sender"].unique()
    )

    age_filter = st.sidebar.selectbox(
        "Age Filter",
        ["All", ">7 Days", ">30 Days"]
    )

    filtered = df[
        (df["Doc Type"].isin(doc_filter)) &
        (df["Status"].isin(status_filter)) &
        (df["Sender"].isin(sender_filter))
    ]

    if age_filter == ">7 Days":
        filtered = filtered[filtered["AgeDays"] > 7]
    elif age_filter == ">30 Days":
        filtered = filtered[filtered["AgeDays"] > 30]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records", len(filtered))
    c2.metric("Open", len(filtered[filtered["Status"] == "Open"]))
    c3.metric("Overdue >7", len(filtered[filtered["AgeDays"] > 7]))
    c4.metric("Avg Age", round(filtered["AgeDays"].mean(), 1))

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Register", "📈 Analytics", "🚨 Exceptions"])

    with tab1:
        st.dataframe(filtered, use_container_width=True)

    with tab2:
        st.subheader("Sender Workload")

        sender = filtered["Sender"].value_counts().reset_index()
        sender.columns = ["Sender", "Count"]

        st.bar_chart(sender.set_index("Sender"))

        st.subheader("Doc Type Split")
        st.bar_chart(filtered["Doc Type"].value_counts())

    with tab3:
        st.subheader("Overdue Items")
        st.dataframe(filtered[filtered["AgeDays"] > 7])

        st.subheader("No Reply Items")
        st.dataframe(filtered[filtered["Reply Date"].isna()])

    st.markdown("---")

    st.subheader("🔎 Drill Down")

    selected = st.selectbox("Select Seq No", filtered["Seq No"].unique())

    st.json(filtered[filtered["Seq No"] == selected].to_dict(orient="records")[0])