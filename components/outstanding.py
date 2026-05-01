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

    # =========================
    # THEME COLORS
    # =========================
    COLORS = {
        "bg": "#0b1220",
        "card": "#0f172a",
        "border": "#334155",
        "open": "#ef4444",
        "out": "#f59e0b",
        "closed": "#22c55e"
    }

    # =========================
    # GLOBAL STYLE (CLEAN + SAFE)
    # =========================
    st.markdown(f"""
    <style>

    /* APP BACKGROUND */
    .stApp {{
        background-color: {COLORS["bg"]};
        color: white;
    }}

    /* FIX COLUMN WIDTH */
    [data-testid="column"] {{
        min-width: 420px !important;
        flex: 0 0 420px !important;
    }}

    /* CARD LOOK */
    div[data-testid="stVerticalBlock"] {{
        background-color: {COLORS["card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 16px;
    }}

    /* KPI METRICS TEXT */
    div[data-testid="metric-container"] {{
        background-color: {COLORS["card"]};
        border: 1px solid {COLORS["border"]};
        padding: 12px;
        border-radius: 12px;
    }}

    /* PLOTLY FIX */
    div[data-testid="stPlotlyChart"] {{
        min-width: 380px !important;
    }}

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # PIE CHART
    # =========================
    def pie(o, out, c):
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            textinfo="label+value",
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="white", width=2)
            ),
            sort=False
        ))

        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font=dict(color="white", size=12)
        )

        return fig

    # =========================
    # KPI CALC (TOTALS)
    # =========================
    def total_metrics():
        return {
            "RFI Open": rfi_open,
            "RFI Outstanding": rfi_out,
            "RFI Closed": rfi_closed,
            "TQ Open": tq_open,
            "TQ Outstanding": tq_out,
            "TQ Closed": tq_closed,
        }

    metrics = total_metrics()


    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("RFI Open", metrics["RFI Open"])
    k2.metric("RFI Outstanding", metrics["RFI Outstanding"])
    k3.metric("RFI Closed", metrics["RFI Closed"])
    k4.metric("TQ Open", metrics["TQ Open"])
    k5.metric("TQ Outstanding", metrics["TQ Outstanding"])
    k6.metric("TQ Closed", metrics["TQ Closed"])

    st.markdown("---")

    # =========================
    # CARD FUNCTION
    # =========================
    def card(title, o, out, c, accent):

        st.markdown(f"### {title} Summary")

        st.markdown(
            f"""
            🔴 **Open:** {o}  
            🟡 **Outstanding:** {out}  
            🟢 **Closed:** {c}
            """
        )

        st.plotly_chart(
            pie(o, out, c),
            use_container_width=True
        )

    # =========================
    # MAIN GRID
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_closed, COLORS["open"])

    with col2:
        card("TQ", tq_open, tq_out, tq_closed, COLORS["out"])