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
    # SEVERITY LOGIC
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
        impact = "High impact"
        note = "May block approvals"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
        impact = "Moderate impact"
        note = "Action required"
    else:
        color = "#facc15"
        status = "MEDIUM"
        impact = "Low risk"
        note = "Monitor"

    # =========================
    # TITLE (COMPACTED)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:6px 8px;
        margin-bottom:4px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:white;
    ">
        🚨 Outstanding (>7 days)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI ROW (COMPACT)
    # =========================
    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.metric(
            label="Overdue",
            value=f"{overdue_total}",
            delta=f"{overdue_pct}%"
        )

    with col2:
        st.markdown(f"""
        <div style="padding-top:2px;">
            <div style="color:{color}; font-weight:700; font-size:12px;">
                {status}
            </div>
            <div style="color:#cbd5e1; font-size:11px;">
                {impact}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # CHART (REDUCED HEIGHT)
    # =========================
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
        height=140,   # ↓ reduced (key change)
        margin=dict(l=15, r=15, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=10),
        xaxis=dict(
            title="Overdue",
            gridcolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # FOOTER (COMPRESSED)
    # =========================
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:2px;
        padding-top:4px;
        border-top:1px solid #1f2937;
    ">
        <span style="color:{color}; font-weight:600;">
            {impact}
        </span>
        — {note}
    </div>
    """, unsafe_allow_html=True)