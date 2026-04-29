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

    def pie(o, out, c):

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
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        return fig

    # =========================
    # TRUE CARD (ALL CONTENT INSIDE ONE CONTAINER)
    # =========================
    def card(title, o, out, c):

        with st.container():

            # FULL CARD BLOCK BACKGROUND FEEL
            st.markdown(f"""
            <div style="
                background:#0f172a;
                border:1px solid #1f2937;
                border-radius:14px;
                padding:12px;
                margin-bottom:14px;
            ">
                <div style="
                    text-align:center;
                    font-size:14px;
                    font-weight:800;
                    color:white;
                    margin-bottom:10px;
                ">
                    {title}
                </div>
            """, unsafe_allow_html=True)

            # KPI TEXT (inside SAME block visually)
            st.markdown(
                f"""
🔴 Open: **{o}**  
🟡 Outstanding: **{out}**  
🟢 Closed: **{c}**
"""
            )

            # PIE INSIDE SAME BLOCK
            st.plotly_chart(
                pie(o, out, c),
                use_container_width=True
            )

            # CLOSE DIV
            st.markdown("</div>", unsafe_allow_html=True)

    # OUTPUT
    card("RFI", rfi_open, rfi_out, rfi_closed)
    card("TQ", tq_open, tq_out, tq_closed)