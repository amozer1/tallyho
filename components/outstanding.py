import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

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
    # HEADER + TOGGLE
    # =========================
    st.markdown("<h1 style='text-align:center;'>Building A – RFI / TQ Overview</h1>", unsafe_allow_html=True)

    _, toggle_col, _ = st.columns([3, 2, 3])
    with toggle_col:
        view = st.radio("", ["RFI", "TQ"], horizontal=True)

    # =========================
    # KPI VALUES BASED ON TOGGLE
    # =========================
    if view == "RFI":
        open_, out_, closed_ = rfi_open, rfi_out, rfi_closed
    else:
        open_, out_, closed_ = tq_open, tq_out, tq_closed

    # =========================
    # KPI CARDS
    # =========================
    def kpi_card(title, value):
        st.markdown(f"""
        <div style="
            padding:18px;
            border-radius:10px;
            border:1px solid #e5e7eb;
            background:white;
            text-align:center;
        ">
            <h4 style="margin-bottom:5px;">{title}</h4>
            <h1 style="margin:0;">{value}</h1>
        </div>
        """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1:
        kpi_card("Open", open_)
    with k2:
        kpi_card("Outstanding", out_)
    with k3:
        kpi_card("Closed", closed_)

    # =========================
    # PIE FUNCTION
    # =========================
    def pie(o, out, c):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="white", width=2)
            ),
            textinfo="percent",
            sort=False
        ))

        fig.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )

        return fig

    # =========================
    # CARD WRAPPER (CLEAN)
    # =========================
    def chart_card(title, fig, key):
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.plotly_chart(fig, use_container_width=True, key=key)

    # =========================
    # PIE ROW (SIDE BY SIDE)
    # =========================
    c1, c2 = st.columns(2, gap="large")

    with c1:
        chart_card("RFI", pie(rfi_open, rfi_out, rfi_closed), "rfi_pie")

    with c2:
        chart_card("TQ", pie(tq_open, tq_out, tq_closed), "tq_pie")

    # =========================
    # TEXT CARDS (BOTTOM)
    # =========================
    b1, b2 = st.columns(2)

    with b1:
        with st.container(border=True):
            st.markdown("### Key Issues")
            st.write("Outstanding RFIs mainly relate to fire strategy and stair pressurisation queries.")
            st.write("**Actions / Owners:** Fire consultant review underway, workshop booked.")

    with b2:
        with st.container(border=True):
            st.markdown("### Notes")
            st.write("Increase driven by façade and interface queries following IFC issue.")
            st.write("**Actions:** Responses due this week, contractor batching queries.")