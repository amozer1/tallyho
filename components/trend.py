import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_rfi_created(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # ONLY VALID DATE FIELD
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df[df["date sent"].notna()].copy()

    # Month bucket (safe + stable)
    df["month"] = df["date sent"].dt.to_period("M").astype(str)

    # =========================
    # FILTER ONLY RFI
    # =========================
    rfi = df[df["doc type"] == "RFI"]

    # Monthly aggregation (pure count)
    rfi_trend = rfi.groupby("month").size().reset_index(name="rfi_created")
    rfi_trend = rfi_trend.sort_values("month")

    # =========================
    # CARD WRAPPER
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
    # STACKED STYLE LINE (FILL + LINE)
    # =========================
    fig = go.Figure()

    # Base filled area (soft stack effect)
    fig.add_trace(go.Scatter(
        x=rfi_trend["month"],
        y=rfi_trend["rfi_created"],
        mode="lines",
        line=dict(color="rgba(31,119,180,0.3)", width=0),
        fill="tozeroy",
        name="RFI Volume (Area)"
    ))

    # Main line
    fig.add_trace(go.Scatter(
        x=rfi_trend["month"],
        y=rfi_trend["rfi_created"],
        mode="lines+markers",
        name="RFI Created",
        line=dict(color="#1f77b4", width=4),
        marker=dict(size=8)
    ))

    # =========================
    # LAYOUT (CLEAN DASHBOARD STYLE)
    # =========================
    fig.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=20, b=40),
        hovermode="x unified",
        xaxis=dict(title="Month"),
        yaxis=dict(title="RFI Created"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # close card
    st.markdown("</div>", unsafe_allow_html=True)