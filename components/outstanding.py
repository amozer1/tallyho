import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    # =========================
    # CALCULATIONS
    # =========================
    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # MATCH AGE_OUTSTANDING CARD EXACT STYLE
    # =========================
    fig = go.Figure()

    # CARD BACKGROUND
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=1, y1=1,
        xref="paper", yref="paper",
        fillcolor="#0f172a",
        line=dict(color="#1f2937"),
        layer="below"
    )

    # TITLE
    fig.add_annotation(
        x=0.5, y=0.9,
        text="<b>🚨 Overdue (&gt;7 days)</b>",
        showarrow=False,
        font=dict(color="#ef4444", size=14),
        xanchor="center"
    )

    # TEXT BLOCKS (structured KPI layout)
    fig.add_annotation(
        x=0.5, y=0.65,
        text=f"Total Overdue: <b>{overdue_total}</b> ({overdue_pct}%)",
        showarrow=False,
        font=dict(color="white", size=12),
        xanchor="center"
    )

    fig.add_annotation(
        x=0.5, y=0.45,
        text=f"TQ Overdue: <b>{overdue_tq}</b> ({tq_pct}%)",
        showarrow=False,
        font=dict(color="#f97316", size=12),
        xanchor="center"
    )

    fig.add_annotation(
        x=0.5, y=0.25,
        text=f"RFI Overdue: <b>{overdue_rfi}</b> ({rfi_pct}%)",
        showarrow=False,
        font=dict(color="#38bdf8", size=12),
        xanchor="center"
    )

    # =========================
    # FIXED SIZE (MATCH AGE CARD)
    # =========================
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)
    