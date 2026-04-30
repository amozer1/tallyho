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
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )

        return fig

    # =========================
    # CARD STYLE (RESTORED BG)
    # =========================
    card_style = """
        <style>
        .custom-card {
            background-color: #1f2937;  /* 👈 previous dark grey */
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    # =========================
    # CARD FUNCTION
    # =========================
    def card(title, o, out, c, key):

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # SIDE BY SIDE CARDS
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_closed, "rfi_pie")

    with col2:
        card("TQ", tq_open, tq_out, tq_closed, "tq_pie")