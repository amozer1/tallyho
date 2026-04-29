import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # REQUIRED COLUMNS
    # =========================
    status_col = "status"
    doc_col = "doc type"
    date_col = "date sent"

    for c in [status_col, doc_col, date_col]:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # COUNTS
    # =========================
    def calc(sub):
        open_ = len(sub[sub[status_col] == "OPEN"])
        closed_ = len(sub[sub[status_col] == "CLOSED"])
        outstanding_ = len(
            sub[
                (sub[status_col] == "OPEN") &
                ((today - sub[date_col]).dt.days > 14)
            ]
        )
        return open_, outstanding_, closed_

    rfi_open, rfi_out, rfi_closed = calc(rfi)
    tq_open, tq_out, tq_closed = calc(tq)

    # =========================
    # COLOURS (STRICT SYSTEM)
    # =========================
    COLORS = {
        "open": "#ef4444",     # red
        "out": "#f59e0b",      # gold
        "closed": "#22c55e"    # green
    }

    # =========================
    # PIE CHART
    # =========================
    def pie(o, out, c, title):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            hole=0,
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            sort=False
        ))

        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        return fig

    # =========================
    # CARD STYLE (NO HTML)
    # =========================
    def render_card(title, o, out, c):

        # CARD HEADER (matches age module style)
        st.markdown(f"""
        <div style="
            background:#0f172a;
            border:1px solid #1f2937;
            border-radius:12px;
            padding:8px 10px;
            margin-bottom:10px;
            text-align:center;
            font-size:13px;
            font-weight:800;
            color:white;
        ">
            {title}
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # CARD BODY (LEFT TEXT + RIGHT PIE)
        # =========================
        col_left, col_right = st.columns([1, 1.6])

        with col_left:
            st.markdown(
                f"""
🔴 Open: **{o}**  
🟡 Outstanding: **{out}**  
🟢 Closed: **{c}**
"""
            )

        with col_right:
            st.plotly_chart(
                pie(o, out, c, title),
                use_container_width=True
            )

        # spacing between cards
        st.markdown("")

    # =========================
    # OPTIONAL KPI TOP BAR
    # =========================
    if total is not None:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total", total)

        with col2:
            st.metric("RFI Items", len(rfi))

        with col3:
            st.metric("TQ Items", len(tq))

        st.markdown("---")

    # =========================
    # OUTPUT CARDS
    # =========================
    render_card("RFI", rfi_open, rfi_out, rfi_closed)
    render_card("TQ", tq_open, tq_out, tq_closed)