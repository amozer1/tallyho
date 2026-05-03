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
        .str.strip()
        .str.upper()
    )

    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # LOGIC
    # =========================
    def calc(sub):

        open_items = sub[sub[status_col] == "OPEN"]
        closed_items = sub[sub[status_col] == "CLOSED"]

        open_count = len(open_items)
        closed_count = len(closed_items)

        outstanding_count = len(
            open_items[
                (open_items[date_col].notna()) &
                ((today - open_items[date_col]).dt.days > 7)
            ]
        )

        return open_count, outstanding_count, closed_count

    rfi_open, rfi_out, rfi_closed = calc(rfi)
    tq_open, tq_out, tq_closed = calc(tq)

    # =========================
    # COLORS
    # =========================
    COLORS = {
        "open": "#ef4444",
        "out": "#f59e0b",
        "closed": "#22c55e"
    }

    # =========================
    # PIE CHART
    # =========================
    def pie(open_count, outstanding, closed):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding (>7d)", "Closed"],
            values=[open_count, outstanding, closed],

            # 🔥 ONLY CHANGE: bigger + clearer text
            textinfo="label+value",
            textfont=dict(size=18, color="white"),
            insidetextorientation="radial",

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
            height=420,
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
    def card(title, open_count, outstanding, closed):

        st.markdown(f"### {title} Overview")

        st.markdown(
            f"""
            🔴 **Open:** {open_count}  
            🟡 **Outstanding (>7d):** {outstanding}  
            🟢 **Closed:** {closed}
            """
        )

        st.markdown("""
        <div style="
            font-size:12px;
            color:#94a3b8;
            margin-top:6px;
            line-height:1.4;
        ">
        <b>Note:</b> Outstanding items are OPEN items older than 7 days.
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            pie(open_count, outstanding, closed),
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