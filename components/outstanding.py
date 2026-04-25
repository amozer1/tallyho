import streamlit as st


def render_outstanding_line(
    overdue,
    total,
    tq_not,
    rfi_not,
    tq_total,
    rfi_total
):

    # =========================
    # SAFETY CHECK
    # =========================
    if total is None or total == 0:
        st.warning("No data available")
        return

    # =========================
    # PERCENTAGES
    # =========================
    overdue_pct = round((overdue / total) * 100, 1)

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0

    total_not = tq_not + rfi_not
    total_not_pct = round((total_not / total) * 100, 1)

    # =========================
    # UI HEADER
    # =========================
    st.markdown(
        """
        <style>
        .outstanding-box {
            background: linear-gradient(90deg, #0f172a, #1e293b);
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #334155;
        }
        .title {
            font-size: 18px;
            font-weight: 600;
            color: #f8fafc;
        }
        .metric {
            font-size: 15px;
            margin-top: 6px;
            color: #cbd5e1;
        }
        .highlight-red {
            color: #ef4444;
            font-weight: 600;
        }
        .highlight-blue {
            color: #3b82f6;
            font-weight: 600;
        }
        .highlight-green {
            color: #22c55e;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # OUTSTANDING BLOCK
    # =========================
    st.markdown(f"""
    <div class="outstanding-box">

        <div class="title">
        ⚠ Outstanding Alerts (7+ Days Aging)
        </div>

        <div class="metric">
        🔴 Overdue Items: <span class="highlight-red">{overdue}</span> ({overdue_pct}%)
        </div>

        <div class="metric">
        ⚡ Total Not Responded: <span class="highlight-red">{total_not}</span> ({total_not_pct}%)
        </div>

        <div class="metric">
        🔵 TQ Not Responded: <span class="highlight-blue">{tq_not}</span> ({tq_not_pct}%)
        </div>

        <div class="metric">
        🟢 RFI Not Responded: <span class="highlight-green">{rfi_not}</span> ({rfi_not_pct}%)
        </div>

    </div>
    """, unsafe_allow_html=True)