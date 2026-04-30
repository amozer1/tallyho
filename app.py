import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

    # =========================
    # GLOBAL SAFE STYLING
    # =========================
    st.markdown("""
        <style>
        /* Card look */
        div[data-testid="stVerticalBlock"] > div {
            background-color: #1f2937;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        }

        /* Reduce spacing inside cards */
        h3 {
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

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
    # SPLIT DATA
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
            height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )

        return fig

    # =========================
    # CARD FUNCTION (SAFE)
    # =========================
    def card(title, o, out, c, key):

        with st.container():

            st.markdown(f"### {title}")

            st.markdown(f"""
🔴 **Open:** {o}  
🟡 **Outstanding:** {out}  
🟢 **Closed:** {c}
""")

            st.markdown("<br>", unsafe_allow_html=True)

            st.plotly_chart(
                pie(o, out, c),
                use_container_width=True,
                key=key
            )

    # =========================
    # SIDE BY SIDE
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_closed, "rfi_pie")

    with col2:
        card("TQ", tq_open, tq_out, tq_closed, "tq_pie")