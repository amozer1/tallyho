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

    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # COUNTS
    # =========================
    def calc(sub):
        open_ = len(sub[sub[status_col] == "OPEN"])
        closed_ = len(sub[sub[status_col] == "CLOSED"])
        out_ = len(
            sub[
                (sub[status_col] == "OPEN") &
                ((today - sub[date_col]).dt.days > 14)
            ]
        )
        return open_, out_, closed_

    rfi_open, rfi_out, rfi_closed = calc(rfi)
    tq_open, tq_out, tq_closed = calc(tq)

    # =========================
    # COLOURS
    # =========================
    COLORS = {
        "open": "#EF4444",
        "out": "#F59E0B",
        "closed": "#22C55E"
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
                line=dict(color="white", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            sort=False
        ))

        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="black"),
            showlegend=False,
            title=dict(text=title, x=0.5)
        )

        return fig

    # =========================
    # CARD STYLE (STREAMLIT ONLY)
    # =========================
    st.markdown(
        """
        <style>
        .card {
            background: white;
            padding: 15px;
            border-radius: 14px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # CARD RENDERER
    # =========================
    def render_card(title, o, out, c):

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f"## {title}")

            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown(f"🔴 Open: **{o}**")
                st.markdown(f"🟡 Outstanding: **{out}**")
                st.markdown(f"🟢 Closed: **{c}**")

            with col2:
                st.plotly_chart(
                    pie(o, out, c, title),
                    use_container_width=True
                )

            st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # OUTPUT
    # =========================
    render_card("RFI", rfi_open, rfi_out, rfi_closed)
    render_card("TQ", tq_open, tq_out, tq_closed)