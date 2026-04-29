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
    # COLUMNS
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
    # SPLIT
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # COUNT LOGIC
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
    # COLOURS (REQUIRED)
    # =========================
    COLORS = {
        "open": "#EF4444",     # red
        "out": "#F59E0B",      # gold
        "closed": "#22C55E"    # green
    }

    # =========================
    # PIE BUILDER
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
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            title=dict(text=title, x=0.5, font=dict(size=16))
        )

        return fig

    # =========================
    # CARD RENDERER
    # =========================
    def render_card(title, o, out, c):

        col_left, col_right = st.columns([1, 1.6])

        with col_left:
            st.markdown(f"### {title}")

            st.markdown(f"🔴 Open: **{o}**")
            st.markdown(f"🟡 Outstanding: **{out}**")
            st.markdown(f"🟢 Closed: **{c}**")

        with col_right:
            st.plotly_chart(
                pie(o, out, c, title),
                use_container_width=True
            )

    # =========================
    # UI LAYOUT (TWO CARDS)
    # =========================
    st.subheader("Document Status Overview")

    render_card("RFI", rfi_open, rfi_out, rfi_closed)
    st.markdown("---")
    render_card("TQ", tq_open, tq_out, tq_closed)