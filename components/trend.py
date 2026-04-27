import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # VALID DATE ONLY
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df[df["date sent"].notna()].copy()

    # Month (STRICTLY from real data)
    df["month"] = df["date sent"].dt.to_period("M").astype(str)

    # =========================
    # FILTER RFI ONLY
    # =========================
    rfi = df[df["doc type"] == "RFI"]

    # Monthly aggregation
    trend = rfi.groupby("month").size().reset_index(name="rfi_created")
    trend = trend.sort_values("month")

    # =========================
    # CARD STYLE
    # =========================
    st.markdown("""
    <div style="
        background: #ffffff;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    ">
    """, unsafe_allow_html=True)

    st.subheader("RFI Created Trend")

    # =========================
    # STACKED STYLE LINE
    # =========================
    fig = go.Figure()

    # soft area fill (visual depth)
    fig.add_trace(go.Scatter(
        x=trend["month"],
        y=trend["rfi_created"],
        mode="lines",
        line=dict(color="rgba(31,119,180,0.25)", width=0),
        fill="tozeroy",
        name="RFI Volume"
    ))

    # main line
    fig.add_trace(go.Scatter(
        x=trend["month"],
        y=trend["rfi_created"],
        mode="lines+markers",
        name="RFI Created",
        line=dict(color="#1f77b4", width=4),
        marker=dict(size=8)
    ))

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=10, b=40),
        hovermode="x unified",
        xaxis=dict(title="Month"),
        yaxis=dict(title="Count"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)