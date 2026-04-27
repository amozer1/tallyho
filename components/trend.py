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

    total = len(df)
    open_count = int(df["is_open"].sum())
    closed_count = int(df["is_closed"].sum())

    # =========================
    # CARD WRAPPER STYLE
    # =========================
    card_container = """
        <div style="
            background: #ffffff;
            padding: 18px;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 18px;
        ">
    """

    card_close = "</div>"

    # =========================
    # TITLE CARD
    # =========================
    st.markdown(card_container, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 5px;
        ">
        RFI / TQ Workflow Intelligence
        </div>

        <div style="
            font-size: 13px;
            color: #6b7280;
        ">
        Live tracking of open vs closed information requests over time
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(card_close, unsafe_allow_html=True)

    # =========================
    # KPI CARDS (INSIDE WRAPPER STYLE)
    # =========================
    kpi_card = """
        <div style="
            background: #f9fafb;
            padding: 16px;
            border-radius: 14px;
            text-align: center;
            box-shadow: inset 0 0 0 1px #e5e7eb;
        ">
            <div style="font-size: 13px; color: #6b7280;">{title}</div>
            <div style="font-size: 24px; font-weight: 700; margin-top: 6px;">
                {value}
            </div>
        </div>
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(kpi_card.format(title="Total Items", value=total), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_card.format(title="Open Items", value=open_count), unsafe_allow_html=True)

    with col3:
        st.markdown(kpi_card.format(title="Closed Items", value=closed_count), unsafe_allow_html=True)

    # =========================
    # CHART INSIDE CARD
    # =========================
    st.markdown(card_container, unsafe_allow_html=True)

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
        title="Workflow Trend (Open vs Closed)",
        xaxis_title="Date Sent",
        yaxis_title="Cumulative Count",
        template="plotly_white",
        height=480,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(card_close, unsafe_allow_html=True)