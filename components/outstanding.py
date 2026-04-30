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
    # PIE (NUMBERS NOT %)
    # =========================
    def pie(o, out, c, color):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],

            # 🔥 SHOW NUMBERS INSTEAD OF %
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
    # CARD HEADER (COLOUR CODED)
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
            font-size:12px;
            font-weight:700;
            color:{color};
        ">
            📊 {title}
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # CARD
    # =========================
    def card(title, o, out, c):

        total = o + out + c

        # 🔥 DYNAMIC COLOR LOGIC
        if title == "RFI":
            color = "#60a5fa"   # blue
        else:
            color = "#f59e0b"   # amber

        # severity override (optional smart touch)
        if o > (0.6 * total):
            color = "#ef4444"  # red alert

        header(f"{title} Outstanding Overview", color)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔴 Open", o)

        with col2:
            st.metric("🟡 Outstanding", out)

        with col3:
            st.metric("🟢 Closed", c)

        st.plotly_chart(
            pie(o, out, c, color),
            use_container_width=True
        )

        st.markdown(f"""
        <div style="
            font-size:11px;
            color:#cbd5e1;
            margin-top:2px;
        ">
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