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
    # SEVERITY LOGIC (for attention)
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
        impact = "High impact on project progress"
        note = "May block approvals and coordination"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
        impact = "Moderate impact on workflow"
        note = "Action required"
    else:
        color = "#facc15"
        status = "MEDIUM"
        impact = "Low risk backlog"
        note = "Monitor"

    # =========================
    # TITLE CARD (MATCH YOUR STYLE)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:8px 10px;
        margin-bottom:6px;
        text-align:center;
        font-size:13px;
        font-weight:800;
        color:white;
    ">
        🚨 Outstanding (>7 days)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # MAIN KPI ROW (NO HTML CARDS)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total Overdue",
            value=f"{overdue_total}",
            delta=f"{overdue_pct}% of total"
        )

    with col2:
        st.markdown(f"""
        <div style="padding-top:6px;">
            <div style="color:{color}; font-weight:800; font-size:13px;">
                {status} RISK
            </div>
            <div style="color:#cbd5e1; font-size:12px;">
                {impact}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # BREAKDOWN CHART (IMPORTANT VISUAL)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ Overdue", "RFI Overdue"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"]),
        text=[
            f"{overdue_tq} ({tq_pct}%)",
            f"{overdue_rfi} ({rfi_pct}%)"
        ],
        textposition="outside"
    ))

    fig.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=11),
        xaxis=dict(
            title="Overdue Items",
            gridcolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(
            showgrid=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # IMPACT FOOTER (CONSEQUENCE LAYER)
    # =========================
    st.markdown(f"""
    <div style="
        font-size:12px;
        color:#cbd5e1;
        margin-top:6px;
        padding-top:6px;
        border-top:1px solid #1f2937;
    ">
        <span style="color:{color}; font-weight:700;">
            {impact}
        </span>
        — {note}
    </div>
    """, unsafe_allow_html=True)