import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date", "status"]

    if not all(col in df.columns for col in required):
        st.error("Missing required columns.")
        return

    # =========================
    # DATA PREP
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)
    combined_total = tq_total + rfi_total

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    overdue = df[df["age"] > 7]
    overdue_count = len(overdue)

    # =========================
    # LAYOUT
    # =========================
    left, right = st.columns([1.7, 1])

    # =========================================================
    # 🟦 LEFT — CAKE KPI CIRCLES
    # =========================================================
    with left:

        st.markdown("### 📊 TQ & RFI Tracker Overview")

        c1, c2, c3 = st.columns(3)

        def cake(value, base, color, label):
            base = base if base > 0 else 1
            pct = round((value / base) * 100, 1)

            fig = go.Figure(go.Pie(
                values=[value, base - value],
                hole=0.68,
                marker=dict(colors=[color, "#eef2f7"]),
                textinfo="none"
            ))

            fig.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

            # CENTER LABEL INSIDE STYLE
            st.markdown(
                f"""
                <div style="text-align:center; margin-top:-15px;">
                    <div style="font-size:14px; color:#6b7280;">
                        {label}
                    </div>
                    <div style="font-size:22px; font-weight:700;">
                        {value}
                    </div>
                    <div style="font-size:13px; color:#9ca3af;">
                        ({pct}%)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c1:
            cake(tq_total, total, "#3b82f6", "TQ Total")

        with c2:
            cake(rfi_total, total, "#f59e0b", "RFI Total")

        with c3:
            cake(combined_total, total, "#22c55e", "Total Workload")

    # =========================================================
    # 🟪 RIGHT — CONTROL PANEL
    # =========================================================
    with right:

        st.markdown("### ⚙ Control Panel")

        st.markdown(f"""
        <div style="
            background:#0f172a;
            color:#f8fafc;
            padding:18px;
            border-radius:14px;
            line-height:2;
        ">

        <div style="font-size:13px; opacity:0.7;">Response Analytics</div>

        🔵 <b>TQ not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br>

        🟠 <b>RFI not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br>

        ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)

        </div>
        """, unsafe_allow_html=True)

    # =========================================================
    # 🟥 FOOTER — RISK STRIP
    # =========================================================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:#fee2e2;
        border-left:6px solid #ef4444;
        padding:14px;
        border-radius:10px;
        font-weight:600;
    ">
    ⚠ Outstanding > 7 Days: {overdue_count} ({round(overdue_count/total*100,1) if total else 0}%)
    </div>
    """, unsafe_allow_html=True)