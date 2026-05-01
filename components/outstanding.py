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

    # =========================
    # SPLIT
    # =========================
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
    # PIE
    # =========================
    def pie(o, out, c):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            textinfo="value",
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="white", width=2)
            ),
            sort=False
        ))

        fig.update_layout(
            height=170,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=11)
        )

        return fig

    # =========================
    # HEADER
    # =========================
    def header(title, color):
        st.markdown(f"""
        <div style="
            background:#0f172a;
            border:1px solid {color};
            border-radius:10px;
            padding:6px 10px;
            margin-bottom:6px;
            text-align:center;
            font-size:13px;
            font-weight:700;
            color:{color};
        ">
            📊 {title}
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # KPI (FIXED WIDTH BOXES — NO SHRINK)
    # =========================
    def kpi_box(label, value, color):
        st.markdown(f"""
        <div style="
            background:#111827;
            border:1px solid #1f2937;
            border-radius:8px;
            padding:6px;
            text-align:center;
            white-space:nowrap;
            min-width:110px;
        ">
            <div style="color:{color}; font-weight:600;">{label}</div>
            <div style="color:white; font-size:14px; font-weight:700;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # CARD
    # =========================
    def card(title, o, out, c):

        total = o + out + c

        color = "#60a5fa" if title == "RFI" else "#f59e0b"
        if o > (0.6 * total):
            color = "#ef4444"

        header(f"{title} Outstanding Overview", color)

        # =========================
        # KPI ROW (STABLE FIX)
        # =========================
        c1, c2, c3 = st.columns([1,1,1], gap="small")

        with c1:
            kpi_box("Open", o, "#ef4444")

        with c2:
            kpi_box("Outstanding", out, "#f59e0b")

        with c3:
            kpi_box("Closed", c, "#22c55e")

        st.plotly_chart(pie(o, out, c), use_container_width=True)

        st.markdown(f"""
        <div style="font-size:12px; color:#cbd5e1;">
            Total items: <b>{total}</b>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # LAYOUT
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_closed)

    with col2:
        card("TQ", tq_open, tq_out, tq_closed)