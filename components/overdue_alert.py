import streamlit as st


def render_overdue_alert(
    overdue,
    total,
    tq_not,
    rfi_not,
    tq_not_pct,
    rfi_not_pct
):

    # =========================
    # SAFETY CHECKS
    # =========================
    if total is None or total == 0:
        st.info("No data available for overdue analysis.")
        return

    overdue = 0 if overdue is None else overdue
    tq_not = 0 if tq_not is None else tq_not
    rfi_not = 0 if rfi_not is None else rfi_not
    tq_not_pct = 0 if tq_not_pct is None else tq_not_pct
    rfi_not_pct = 0 if rfi_not_pct is None else rfi_not_pct

    overdue_pct = round((overdue / total) * 100, 1)

    # =========================
    # SEVERITY LOGIC
    # =========================
    if overdue_pct < 20:
        color = "#22c55e"   # green
        label = "LOW RISK"
    elif overdue_pct < 40:
        color = "#f59e0b"   # amber
        label = "MEDIUM RISK"
    else:
        color = "#ef4444"   # red
        label = "HIGH RISK"

    # =========================
    # ALERT BOX (SAFE STREAMLIT RENDER)
    # =========================
    st.markdown(
        f"""
        <div style="
            padding: 14px 16px;
            border-radius: 12px;
            background: rgba(0,0,0,0.35);
            border: 2px solid {color};
            max-width: 600px;
            margin-bottom: 10px;
        ">
            <div style="
                color:{color};
                font-weight:900;
                font-size:16px;
                display:flex;
                justify-content:space-between;
            ">
                <span>⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)</span>
                <span>{label}</span>
            </div>

            <div style="
                margin-top:10px;
                color:white;
                font-size:13px;
                line-height:1.7;
            ">
                🔵 TQ: {tq_not} ({tq_not_pct}%)<br>
                🟢 RFI: {rfi_not} ({rfi_not_pct}%)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# OPTIONAL TABLE VIEW
# =========================
def render_overdue_button(df):

    if df is None or df.empty:
        return

    if st.button("🔍 View Overdue Items (>7 Days)"):

        overdue_df = df[
            (df["reply date"].isna()) &
            (df["age"] > 7)
        ]

        st.markdown("### 🔴 Overdue Records")
        st.dataframe(overdue_df, use_container_width=True)