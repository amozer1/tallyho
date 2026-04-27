import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available for trend analysis.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # DATE HANDLING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    df["month_sent"] = df["date sent"].dt.to_period("M").astype(str)
    df["month_closed"] = df["reply date"].dt.to_period("M").astype(str)

    # =========================
    # SPLIT TYPES
    # =========================
    rfi = df[df["doc type"] == "RFI"]
    tq = df[df["doc type"] == "TQ"]

    # =========================
    # AGGREGATION FUNCTION
    # =========================
    def build_series(data, sent_col, closed_col):

        raised = data.groupby(sent_col).size().reset_index(name="raised")

        closed = (
            data[data["status"].str.lower() == "closed"]
            .groupby(closed_col)
            .size()
            .reset_index(name="closed")
        )

        merged = pd.merge(raised, closed, left_on=sent_col, right_on=closed_col, how="outer").fillna(0)

        merged["month"] = merged[sent_col].fillna(merged[closed_col])
        merged = merged.sort_values("month")

        return merged

    rfi_ts = build_series(rfi, "month_sent", "month_closed")
    tq_ts = build_series(tq, "month_sent", "month_closed")

    # =========================
    # SMALL LINE CHART
    # =========================
    def sparkline(x, y):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=2)
        ))

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=20, b=10),
            template="plotly_white",
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title=None, showgrid=False),
            showlegend=False
        )

        return fig

    # =========================
    # 4-COLUMN LAYOUT
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**RFI Raised**")
        st.plotly_chart(
            sparkline(rfi_ts["month"], rfi_ts["raised"]),
            use_container_width=True
        )

    with col2:
        st.markdown("**RFI Closed**")
        st.plotly_chart(
            sparkline(rfi_ts["month"], rfi_ts["closed"]),
            use_container_width=True
        )

    with col3:
        st.markdown("**TQ Raised**")
        st.plotly_chart(
            sparkline(tq_ts["month"], tq_ts["raised"]),
            use_container_width=True
        )

    with col4:
        st.markdown("**TQ Closed**")
        st.plotly_chart(
            sparkline(tq_ts["month"], tq_ts["closed"]),
            use_container_width=True
        )