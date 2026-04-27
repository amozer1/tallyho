import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # =========================
    # CLEAN FIELDS
    # =========================
    required = ["doc type", "date sent", "reply date", "status"]
    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div style="
        text-align:center;
        font-size:14px;
        font-weight:800;
        color:#E2E8F0;
        margin-bottom:10px;
    ">
        📊 TQ / RFI Tracker
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # FIGURE
    # =========================
    fig = go.Figure()

    fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",

        xaxis=dict(
            visible=False,
            range=[0, 3],
            fixedrange=True
        ),

        yaxis=dict(
            visible=False,
            range=[-0.2, 1.2],
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1
        )
    )

    # =========================
    # CIRCLES (BIGGER + BALANCED)
    # =========================
    circles = [
        (0.1, 0.05, 0.95, 0.95, "rgba(59,130,246,0.22)", "#60A5FA"),   # TQ
        (1.05, 0.05, 1.95, 0.95, "rgba(168,85,247,0.25)", "#A855F7"),  # TOTAL
        (2.0, 0.05, 2.9, 0.95, "rgba(34,197,94,0.22)", "#4ADE80")      # RFI
    ]

    for x0, y0, x1, y1, fill, line in circles:
        fig.add_shape(
            type="circle",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=fill,
            line=dict(color=line, width=2)
        )

    # =========================
    # CENTERS
    # =========================
    tq_x, tq_y = 0.55, 0.5
    total_x, total_y = 1.5, 0.5
    rfi_x, rfi_y = 2.45, 0.5

    # =========================
    # SAFE TEXT BLOCK
    # =========================
    def add_block(x, y, title, pct, count, color):

        fig.add_annotation(
            x=x, y=y+0.10,
            text=f"<b>{title}</b>",
            showarrow=False,
            font=dict(color=color, size=13)
        )

        fig.add_annotation(
            x=x, y=y,
            text=f"<b>{pct}%</b>",
            showarrow=False,
            font=dict(color="white", size=22)
        )

        fig.add_annotation(
            x=x, y=y-0.10,
            text=f"<b>{count}</b>",
            showarrow=False,
            font=dict(color="white", size=26)
        )

    # =========================
    # KPI BLOCKS
    # =========================
    add_block(tq_x, tq_y, "TQ Only", tq_pct, tq_total, "#60A5FA")
    add_block(total_x, total_y, "TQ + RFI", 100, total, "#A855F7")
    add_block(rfi_x, rfi_y, "RFI Only", rfi_pct, rfi_total, "#4ADE80")

    # =========================
    # NOT RESPONDED (SAFE INSIDE CARD)
    # =========================
    fig.add_annotation(
        x=tq_x, y=0.05,
        text=f"TQ Not Responded: {tq_not}",
        showarrow=False,
        font=dict(color="#60A5FA", size=10)
    )

    fig.add_annotation(
        x=total_x, y=0.05,
        text=f"Total Not Responded: {total_not}",
        showarrow=False,
        font=dict(color="#A855F7", size=10)
    )

    fig.add_annotation(
        x=rfi_x, y=0.05,
        text=f"RFI Not Responded: {rfi_not}",
        showarrow=False,
        font=dict(color="#4ADE80", size=10)
    )

    # =========================
    # RENDER
    # =========================
    st.plotly_chart(fig, use_container_width=True)