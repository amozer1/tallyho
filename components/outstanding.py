import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    status_col = "status"
    doc_col = "doc type"
    date_col = "date sent"

    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

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

    COLORS = {
        "open": "#ef4444",
        "out": "#f59e0b",
        "closed": "#22c55e"
    }

    # =========================
    # PIE CHART
    # =========================
    def pie(o, out, c):
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            textinfo="label+value",
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="white", width=2)
            ),
            sort=False
        ))

        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=12)
        )

        return fig

    # =========================
    # KPI CARD STYLE
    # =========================
    def kpi_card(label, value, color):
        st.markdown(f"""
        <div style="
            background:#0f172a;
            border:1px solid {color};
            padding:12px;
            border-radius:12px;
            text-align:center;
        ">
            <div style="font-size:13px; color:#cbd5e1;">{label}</div>
            <div style="font-size:22px; font-weight:700; color:white;">
                {value}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # SECTION CARD
    # =========================
    def section(title, o, out, c):

        st.markdown(f"### {title}")

        # KPI ROW (CLEAN BLOCKS)
        k1, k2, k3 = st.columns(3)

        with k1:
            kpi_card("Open", o, COLORS["open"])

        with k2:
            kpi_card("Outstanding (>14 days)", out, COLORS["out"])

        with k3:
            kpi_card("Closed", c, COLORS["closed"])

        st.plotly_chart(
            pie(o, out, c),
            use_container_width=True
        )

        st.divider()

    # =========================
    # LAYOUT
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        section("RFI", rfi_open, rfi_out, rfi_closed)

    with col2:
        section("TQ", tq_open, tq_out, tq_closed)