import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# MUST MATCH APP.PY SIGNATURE
def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # REQUIRED COLUMNS (LOWERCASE BECAUSE YOU NORMALISE IN APP.PY)
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
    # SPLIT DATA
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # COUNTS FUNCTION
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
    # COLOURS (STRICT)
    # =========================
    colors = {
        "open": "#EF4444",
        "out": "#F59E0B",
        "closed": "#22C55E"
    }

    # =========================
    # PIE BUILDER (SOLID)
    # =========================
    def pie(title, o, out, c):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            hole=0,
            marker=dict(
                colors=[colors["open"], colors["out"], colors["closed"]],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+percent",
            textposition="inside",
            sort=False
        ))

        fig.update_layout(
            title=dict(text=title, x=0.5),
            height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        return fig

    # =========================
    # TOP KPI (USES YOUR TOTAL ARG)
    # =========================
    if total is not None:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Items", total)

        with col2:
            st.metric("RFI Items", len(rfi))

        with col3:
            st.metric("TQ Items", len(tq))

    st.markdown("---")

    # =========================
    # PIES (MATCH YOUR APP LAYOUT)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("RFI Status")
        st.plotly_chart(pie("RFI", rfi_open, rfi_out, rfi_closed), use_container_width=True)

    with col2:
        st.subheader("TQ Status")
        st.plotly_chart(pie("TQ", tq_open, tq_out, tq_closed), use_container_width=True)