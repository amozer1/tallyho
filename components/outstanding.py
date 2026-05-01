import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    # =========================
    # GLOBAL CSS (SAFE ONLY)
    # =========================
    st.markdown("""
    <style>

    /* FIX COLUMN WIDTH */
    [data-testid="column"] {
        min-width: 420px !important;
        flex: 0 0 420px !important;
    }

    /* PREVENT PLOTLY SHRINKING */
    div[data-testid="stPlotlyChart"] {
        min-width: 380px !important;
    }

    </style>
    """, unsafe_allow_html=True)

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
    # PIE (FIXED SIZE)
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
            height=240,
            width=380,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=12)
        )

        return fig

    # =========================
    # CARD (STREAMLIT ONLY)
    # =========================
    def card(title, o, out, c):

        total = o + out + c
        color = "#60a5fa" if title == "RFI" else "#f59e0b"

        if o > (0.6 * total):
            color = "#ef4444"

        # REAL STREAMLIT CARD
        with st.container():

            st.markdown(f"""
            <div style="
                border:1px solid {color};
                border-radius:14px;
                padding:12px;
                background:#0f172a;
            ">
            """, unsafe_allow_html=True)

            st.markdown(f"### 📊 {title} Outstanding Overview")

            # KPI ROW
            k1, k2, k3 = st.columns(3)

            with k1:
                st.markdown(f"🔴 Open: **{o}**")

            with k2:
                st.markdown(f"🟡 Outstanding: **{out}**")

            with k3:
                st.markdown(f"🟢 Closed: **{c}**")

            # PIE (NOW ALWAYS INSIDE STREAMLIT FLOW)
            st.plotly_chart(
                pie(o, out, c),
                use_container_width=False
            )

            st.markdown(f"**Total items:** {total}")

            st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # LAYOUT
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_closed)

    with col2:
        card("TQ", tq_open, tq_out, tq_closed)