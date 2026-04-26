import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN DETECTION
    # =========================
    def find_col(name):
        for c in df.columns:
            if c.strip().lower() == name.lower():
                return c
        return None

    status_col = find_col("status")
    doc_col = find_col("doc type")
    date_col = find_col("date sent")

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # OUTSTANDING LOGIC
    # =========================
    open_df = df[df[status_col] == "OPEN"]

    overdue_df = open_df[
        (today - open_df[date_col]).dt.days > 7
    ]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df[doc_col] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df[doc_col] == "RFI"])

    # =========================
    # SEVERITY (SAME STYLE LOGIC)
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
    else:
        color = "#facc15"
        status = "MEDIUM"

    # =========================
    # CENTERED CARD LAYOUT (LIKE AGE OUTSTANDING)
    # =========================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # =========================
        # TITLE CARD
        # =========================
        st.markdown(f"""
        <div style="
            background:#0f172a;
            border:1px solid #1f2937;
            border-radius:12px;
            padding:8px 10px;
            margin-bottom:6px;
            text-align:center;
            font-size:13px;
            font-weight:800;
            color:{color};
        ">
            🚨 Outstanding (>7 Days) — {status}
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # MAIN CHART (PRIMARY VISUAL)
        # =========================
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=[overdue_tq, overdue_rfi],
            y=["TQ Overdue", "RFI Overdue"],
            orientation="h",
            marker=dict(color=["#f97316", "#38bdf8"]),
            text=[overdue_tq, overdue_rfi],
            textposition="outside",
            hovertemplate="Items: %{x}<extra></extra>"
        ))

        fig.update_layout(
            height=200,
            margin=dict(l=25, r=25, t=10, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            bargap=0.35,
            font=dict(color="white", size=11),

            xaxis=dict(
                title="Overdue Items",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",
                zeroline=True,
                zerolinecolor="rgba(255,255,255,0.35)",
                linecolor="rgba(255,255,255,0.25)",
                tickfont=dict(color="white"),
                title_font=dict(color="white")
            ),

            yaxis=dict(
                showgrid=False,
                tickfont=dict(color="white")
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # FOOTER SUMMARY (LIKE AGE OUTSTANDING STYLE)
        # =========================
        st.markdown(
            f"**Total Overdue:** {overdue_total} ({overdue_pct}%)  |  "
            f"**TQ:** {overdue_tq}  |  **RFI:** {overdue_rfi}"
        )