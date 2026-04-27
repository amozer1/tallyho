import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMNS
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    if "date sent" not in df.columns or "status" not in df.columns:
        st.error("Missing required columns: 'date sent' or 'status'")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df.dropna(subset=["date sent"])

    df["status"] = df["status"].fillna("").str.lower()

    df["is_open"] = df["status"].eq("open")
    df["is_closed"] = df["status"].eq("closed")

    # =========================
    # SORT + CUMULATIVE FLOW
    # =========================
    df_sorted = df.sort_values("date sent")

    df_sorted["open_cum"] = df_sorted["is_open"].cumsum()
    df_sorted["closed_cum"] = df_sorted["is_closed"].cumsum()

    # =========================
    # TREND LINE
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["open_cum"],
        mode="lines+markers",
        name="Open Items"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["closed_cum"],
        mode="lines+markers",
        name="Closed Items"
    ))

    fig.update_layout(
        title="RFI / TQ Workflow Trend",
        xaxis_title="Date Sent",
        yaxis_title="Cumulative Count",
        template="plotly_white",
        height=480,
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # KPI CARDS (CONSISTENT UI)
    # =========================
    total = len(df)
    open_count = int(df["is_open"].sum())
    closed_count = int(df["is_closed"].sum())

    card_style = """
        <div style="
            background: #ffffff;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <div style="font-size: 14px; color: #6b7280;">{title}</div>
            <div style="font-size: 26px; font-weight: 700; margin-top: 6px;">
                {value}
            </div>
        </div>
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(card_style.format(title="Total Items", value=total), unsafe_allow_html=True)

    with col2:
        st.markdown(card_style.format(title="Open Items", value=open_count), unsafe_allow_html=True)

    with col3:
        st.markdown(card_style.format(title="Closed Items", value=closed_count), unsafe_allow_html=True)