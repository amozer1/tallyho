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
    # OVERDUE (>7 DAYS)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # SEVERITY
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
        impact = "High impact on delivery"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
        impact = "Moderate risk"
    else:
        color = "#facc15"
        status = "MEDIUM"
        impact = "Monitor"

    # =========================
    # OUTER CARD (ALL CONTENT INSIDE)
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:10px;
    ">
    """, unsafe_allow_html=True)

    # TITLE (INSIDE CARD)
    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:{color};
        margin-bottom:6px;
    ">
        🚨 Outstanding (>7 days) — {status}
    </div>
    """, unsafe_allow_html=True)

    # KPI
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Overdue", f"{overdue_total}", f"{overdue_pct}%")

    with col2:
        st.markdown(f"""
        <div style="
            font-size:12px;
            color:#cbd5e1;
            padding-top:6px;
        ">
            {impact}
        </div>
        """, unsafe_allow_html=True)

    # CHART (STATIC)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ", "RFI"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"]),
        text=[overdue_tq, overdue_rfi],
        textposition="outside"
    ))

    fig.update_layout(
        height=140,
        margin=dict(l=10, r=10, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

    # FOOTER INSIDE CARD
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:4px;
        border-top:1px solid #1f2937;
        padding-top:4px;
    ">
        TQ: {overdue_tq} ({tq_pct}%) |
        RFI: {overdue_rfi} ({rfi_pct}%)
    </div>
    """, unsafe_allow_html=True)

    # CLOSE CARD
    st.markdown("</div>", unsafe_allow_html=True)