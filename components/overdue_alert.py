import streamlit as st


def render_overdue_alert(overdue, total, tq_not, rfi_not, tq_not_pct, rfi_not_pct):

    if total == 0:
        return

    overdue_pct = round((overdue / total) * 100, 1)

    # risk colour
    color = "#ef4444" if overdue_pct >= 40 else "#f59e0b" if overdue_pct >= 20 else "#22c55e"
    label = "HIGH RISK" if overdue_pct >= 40 else "MEDIUM RISK" if overdue_pct >= 20 else "LOW RISK"

    html = f"""
    <div style="
        padding:14px 16px;
        border-radius:12px;
        background:rgba(0,0,0,0.35);
        border:2px solid {color};
        max-width:650px;
    ">

        <div style="
            display:flex;
            justify-content:space-between;
            font-weight:900;
            font-size:16px;
            color:{color};
            margin-bottom:6px;
        ">
            <span>⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)</span>
            <span>{label}</span>
        </div>

        <div style="
            color:white;
            font-size:13px;
            line-height:1.7;
            border-top:1px solid rgba(255,255,255,0.15);
            padding-top:8px;
        ">
            🔵 TQ Not Responded: {tq_not} ({tq_not_pct}%)<br>
            🟢 RFI Not Responded: {rfi_not} ({rfi_not_pct}%)
        </div>

    </div>
    """

    # IMPORTANT (this is what fixes your issue)
    st.markdown(html, unsafe_allow_html=True)