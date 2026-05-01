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

    df[status_col] = (
        df[status_col]
        .astype(str)
        .str.replace("\xa0", "", regex=False)
        .str.strip()
        .str.upper()
    )

    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # FINAL LOGIC (CORRECT)
    # =========================
    def calc(sub):

        closed = len(sub[sub[status_col] == "CLOSED"])

        open_items = sub[sub[status_col] == "OPEN"]

        open_count = len(open_items)

        outstanding = len(
            open_items[
                (open_items[date_col].notna()) &
                ((today - open_items[date_col]).dt.days > 7)
            ]
        )

        return open_count, outstanding, closed

    rfi_open, rfi_out, rfi_closed = calc(rfi)
    tq_open, tq_out, tq_closed = calc(tq)

    # =========================
    # COLOURS
    # =========================
    COLORS = {
        "open": "#ef4444",     # 🔴 red
        "out": "#f59e0b",      # 🟡 gold
        "closed": "#22c55e"    # 🟢 green
    }

    # =========================
    # PIE (NO DOUBLE COUNTING)
    # =========================
    def pie(o, out, c):

        fresh_open = o - out

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open (≤7d)", "Outstanding (>7d)", "Closed"],
            values=[fresh_open, out, c],
            textinfo="label+value",
            marker=dict(
                colors=[
                    COLORS["open"],
                    COLORS["out"],
                    COLORS["closed"]
                ],
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
    # CARD
    # =========================
    def card(title, o, out, c):

        st.markdown(f"### {title} Overview")

        st.markdown(
            f"""
            🔴 **Open:** {o}  
            🟡 **Outstanding (>7d):** {out}  
            🟢 **Closed:** {c}
            """
        )

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
        card("RFI", rfi_open, rfi_out, rfi_closed)

    with col2:
        card("TQ", tq_open, tq_out, tq_closed)