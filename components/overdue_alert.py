import streamlit as st


def render_overdue_alert(overdue, total, tq_not, rfi_not, tq_not_pct, rfi_not_pct):

    # =========================
    # SAFETY CHECK
    # =========================
    if total is None or total == 0:
        st.info("No data available for overdue alert.")
        return

    # =========================
    # CALCULATIONS
    # =========================
    overdue_pct = round((overdue / total) * 100, 1)

    # =========================
    # SEVERITY LOGIC
    # =========================
    if overdue_pct < 20:
        color = "#22c55e"
        label = "LOW RISK"
    elif overdue_pct < 40:
        color = "#f59e0b"
        label = "MEDIUM RISK"
    else:
        color = "#ef4444"
        label = "HIGH RISK"

    # =========================
    # SAFE STREAMLIT RENDER (NO RAW HTML ISSUES)
    # =========================
    st.markdown(
        f"""
        <div style="
            padding: 14px 16px;
            border-radius: 12px;
            background: rgba(0,0,0,0.35);
            border: 2px solid {color};
            max-width: 650px;
        ">

            <div style="
                display: flex;
                justify-content: space-between;
                font-weight: 900;
                font-size: 16px;
                color: {color};
                margin-bottom: 6px;
            ">
                <span>⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)</span>
                <span>{label}</span>
            </div>

            <div style="
                color: white;
                font-size: 13px;
                line-height: 1.7;
                border-top: 1px solid rgba(255,255,255,0.15);
                padding-top: 8px;
                margin-top: 6px;
            ">
                🔵 TQ Not Responded: {tq_not} ({tq_not_pct}%)<br>
                🟢 RFI Not Responded: {rfi_not} ({rfi_not_pct}%)
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )