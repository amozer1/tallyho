import streamlit as st


def render_outstanding_line(df, total):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or total == 0:
        st.warning("No data available")
        return

    # =========================
    # CLEANING (ensure consistency)
    # =========================
    df = df.copy()
    df["doc type"] = df["doc type"].astype(str).str.lower()

    # =========================
    # OVERDUE FILTER (> 7 DAYS + NOT REPLIED)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue = len(overdue_df)
    overdue_pct = round((overdue / total) * 100, 1)

    # =========================
    # BREAKDOWN (FROM REAL DATA)
    # =========================
    tq_total = len(df[df["doc type"] == "tq"])
    rfi_total = len(df[df["doc type"] == "rfi"])

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "tq"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "rfi"])

    tq_pct = round((overdue_tq / tq_total) * 100, 1) if tq_total else 0
    rfi_pct = round((overdue_rfi / rfi_total) * 100, 1) if rfi_total else 0

    # =========================
    # UI OUTPUT (SIMPLE + CLEAR)
    # =========================
    st.markdown(f"""
### ⚠ Overdue (> 7 Days)

🔴 **Overdue = {overdue} ({overdue_pct}%)**

➡ TQ overdue: **{overdue_tq} ({tq_pct}%)**  
➡ RFI overdue: **{overdue_rfi} ({rfi_pct}%)**
""")