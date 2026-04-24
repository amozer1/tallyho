import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TQ / RFI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")

    # clean column names
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]

    rename_map = {
        "Doc Type": "Type",
        "Date of reply (CDE)": "Reply Date",
        "Date reply required by": "Required Date",
        "Date Sent": "Date Sent",
        "Period (Wks)": "Period"
    }
    df.rename(columns=rename_map, inplace=True)

    # convert dates
    for col in ["Date Sent", "Required Date", "Reply Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # status
    today = pd.Timestamp.today()

    df["Status"] = "Open"
    df.loc[df["Reply Date"].notna(), "Status"] = "Closed"
    df.loc[(df["Required Date"] < today) & (df["Reply Date"].isna()), "Status"] = "Overdue"

    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Filters")

type_filter = st.sidebar.multiselect(
    "Type", options=df["Type"].unique(), default=df["Type"].unique()
)

originator_filter = st.sidebar.multiselect(
    "Originator", options=df["Originator"].dropna().unique(), default=df["Originator"].dropna().unique()
)

recipient_filter = st.sidebar.multiselect(
    "Recipient", options=df["Recipient"].dropna().unique(), default=df["Recipient"].dropna().unique()
)

status_filter = st.sidebar.multiselect(
    "Status", options=df["Status"].unique(), default=df["Status"].unique()
)

filtered_df = df[
    (df["Type"].isin(type_filter)) &
    (df["Originator"].isin(originator_filter)) &
    (df["Recipient"].isin(recipient_filter)) &
    (df["Status"].isin(status_filter))
]

# ---------------- KPI CARDS ----------------
total_rfi = len(filtered_df[filtered_df["Type"] == "RFI"])
total_tq = len(filtered_df[filtered_df["Type"] == "TQ"])
open_items = len(filtered_df[filtered_df["Status"] == "Open"])
closed_items = len(filtered_df[filtered_df["Status"] == "Closed"])
overdue_items = len(filtered_df[filtered_df["Status"] == "Overdue"])
avg_period = round(filtered_df["Period"].replace(0, pd.NA).mean(), 2)

st.title("📊 TQ / RFI Dashboard")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("RFIs", total_rfi)
c2.metric("TQs", total_tq)
c3.metric("Open", open_items)
c4.metric("Closed", closed_items)
c5.metric("Overdue", overdue_items)
c6.metric("Avg Weeks", avg_period)

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        filtered_df,
        names="Type",
        title="RFI vs TQ"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered_df,
        names="Status",
        title="Status Distribution",
        hole=0.5
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TREND ----------------
trend = filtered_df.groupby(filtered_df["Date Sent"].dt.date).size().reset_index(name="Count")

fig3 = px.line(
    trend,
    x="Date Sent",
    y="Count",
    title="Queries Sent Over Time",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- RECIPIENT LOAD ----------------
recipient_load = filtered_df.groupby("Recipient").size().reset_index(name="Count")

fig4 = px.bar(
    recipient_load,
    x="Recipient",
    y="Count",
    title="Recipient Workload"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- TABLE ----------------
st.subheader("Detailed Log")
st.dataframe(filtered_df, use_container_width=True)